---
title: Java8 Stream 使用 groupingBy
comments: true
date: 2022-07-19 18:15:50
categories: java
tags:
  - Stream
---
# groupingBy只进行分组
```java

/**
 * 使用java8 stream groupingBy操作,按城市分组list
 */
public void groupingByCity() {
  Map<String, List<Employee>> map = employees.stream().collect(Collectors.groupingBy(Employee::getCity));

  map.forEach((k, v) -> {
    System.out.println(k + " = " + v);
  });
}
```

# groupingBy分组并进行统计
```java

/**
 * 使用java8 stream groupingBy操作,按城市分组list统计count
 */
public void groupingByCount() {
  Map<String, Long> map = employees.stream()
      .collect(Collectors.groupingBy(Employee::getCity, Collectors.counting()));

  map.forEach((k, v) -> {
    System.out.println(k + " = " + v);
  });
}
```

# groupingBy分组后针对进行求和
```java
/**
	 * 使用java8 stream groupingBy操作,按城市分组list并计算分组销售总值
	 */
public void groupingBySum() {
  Map<String, Long> map = employees.stream()
      .collect(Collectors.groupingBy(Employee::getCity, Collectors.summingLong(Employee::getAmount)));

  map.forEach((k, v) -> {
    System.out.println(k + " = " + v);
  });

  // 对Map按照分组销售总值逆序排序
  Map<String, Long> sortedMap = new LinkedHashMap<>();
  map.entrySet().stream().sorted(Map.Entry.<String, Long> comparingByValue().reversed())
      .forEachOrdered(e -> sortedMap.put(e.getKey(), e.getValue()));

  sortedMap.forEach((k, v) -> {
    System.out.println(k + " = " + v);
  });
}
```