---
title: 权重随机算法
date: 2020-08-08 21:34:36
tags:
	- 算法
    - Java
categories:
  - 算法
---
>   在平时生活中我们往往会遇到一些权重选择的场景，如**广告投放**按照不同广告的权重比进行投放，**流量负载**也需要根据不同的权重选择不同策略。

假如有4个元素A,B,C,D权重分别是1,2,3,4 ，随机请求的结果，命中各个元素的比例需要是1:2:3:4，那么我们可以先绘制一个第一象限的数轴，然后依据权重比例，分别在坐标轴上找出每个权重累加后对应的点。

![image-20210812193417818](http://images.marcus659.com/typora/weight-section.png)

试想一下，如果我们的所有请求均散落在区间[0,10)中，那么每个区间散落的散点比例，则应该正好是我们每个元素之间的权重比例。

根据上面的绘图和思考，我们来总结一下思路：

1. 依次累加权重，在散落区间中确定在数轴上的坐标点
2. 绘制一条第一象限坐标，此处我们使用`SortedMap`的实现类`TreeMap`进行实现
3. 按照顺序在坐标轴上进行标点，也就是每个点都是`TreeMap`中的一个Entry，且是从小到大的排列顺序(`TreeMap`是红黑树)
4. 在`TreeMap`中key为权重叠加的值，value是权重的标识
5. 使用随机函数进行区间落点，请求散点期待正态分布，散点均匀
6. 利用treemap.tailMap().firstKey()即可找到目标元素
7. 也可以使用数组+二分法实现
<!--more-->
### 使用TreeMap实现

1. 声明一个权重随机类，`累加权重值`，`构建顺序区间`，`区间随机落点`

```java
import javafx.util.Pair;
import org.assertj.core.util.Preconditions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Objects;
import java.util.SortedMap;
import java.util.TreeMap;

/**
 * 权重随机算法
 *
 * @author Lovel
 * @date 2021/7/8-0:06
 */
public class WeightRandom<K, V extends Number> {
    // 顺序区间构建
    private final TreeMap<Double, K> weightMap = new TreeMap<>();
    private static final Logger logger = LoggerFactory.getLogger(WeightRandom.class);

    public WeightRandom(List<Pair<K, V>> list) {
        // 权重和标识的 key-value 集合校验
        Objects.requireNonNull(list, "list can NOT be null!");
        for (Pair<K, V> pair : list) {
            Preconditions.checkArgument(pair.getValue().doubleValue() > 0, String.format("非法权重值：pair=%s", pair));
            double lastWeight = this.weightMap.size() == 0 ? 0 : this.weightMap.lastKey();// 权重值统一转为double
            this.weightMap.put(pair.getValue().doubleValue() + lastWeight, pair.getKey());// 权重值累加
        }
        logger.info("Weight interval construction is completed. {}", weightMap);
    }

    public K random() {
        // 延伸 [0,1) 区间到权重区间
        double randomWeight = this.weightMap.lastKey() * Math.random();
        // 根据随机散落区间的坐标，找到落点值到区间最大值的子区间，以下两行代码主要利用treemap.tailMap().firstKey()即可找到目标元素
        SortedMap<Double, K> tailMap = this.weightMap.tailMap(randomWeight);
        // 返回子区间最小值的标的
        return this.weightMap.get(tailMap.firstKey());
    }
}
```

2. 权重测试类，`声明标识与权重占比`,`随机`

```java
import javafx.util.Pair;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author Lovel
 * @date 2021/7/8-0:09
 */
public class WeightRandomTest {
    // 权重标识-占比的 key-value 集合
    static List<Pair<String, Integer>> list;
    // 随机权重区间
    private static WeightRandom<String, Integer> random;
    private static Logger logger = LoggerFactory.getLogger(WeightRandomTest.class);


    public static void main(String[] args) {
        Map<String, Integer> countMap = new HashMap<>();
        for (int i = 0; i < 100000000; i++) {
            // 利用 treeMap 的 tailMap 和 lastKey 找到区间
            String randomKey = random.random();
            countMap.put(randomKey, countMap.getOrDefault(randomKey, 0) + 1);
        }
        //遍历100000000次落点后的权重结果
        for (Pair<String, Integer> pair : list) {
            logger.debug("{}:{}", pair.getKey(), countMap.get(pair.getKey()));
        }
    }
    static {

        list = new ArrayList<>();
        list.add(new Pair("A", 1));
        list.add(new Pair("B", 2));
        list.add(new Pair("C", 3));
        list.add(new Pair("D", 4));
        //list.add(new Pair("E", 0));
        random = new WeightRandom(list);
    }
}

```

