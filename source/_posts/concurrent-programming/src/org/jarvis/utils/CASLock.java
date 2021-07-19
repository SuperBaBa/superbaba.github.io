package org.jarvis.utils;

import sun.misc.Unsafe;

import java.lang.reflect.Field;

/**
 * 使用cas机制实现一把锁
 *
 * @author tennyson
 * @date 2021/4/23-11:10
 */
public class CASLock {
    /**
     * 定义个一个锁状态status，要求所有内存均可见
     */
    private volatile int status;
    /**
     * 获取unSafe对象
     */
    private static final Unsafe unsafe = getUnsafe();
    /**
     * 由于CAS需要一个地址，定义此变量用于表示status在内存中的地址
     */
    private static long valueOffset = 0;

    static {
        try {
            //初始化status在内存中的地址
            valueOffset = unsafe.objectFieldOffset(CASLock.class.getDeclaredField("status"));
        } catch (NoSuchFieldException e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取Unsafe对象
     *
     * @return
     */
    public static Unsafe getUnsafe() {
        try {
            /*
             *theUnsafe是Unsafe类中的静态成员变量，其也是在类加载时，静态代码块初始化的成员变量
             */
            Field field = Unsafe.class.getDeclaredField("theUnsafe");
            field.setAccessible(true);
            return (Unsafe) field.get(null);

        } catch (Exception e) {
        }
        return null;
    }

    public void lock() {
        //如果不能获取到锁则自旋
        while (!compareAndSwapSet(0, 1)) {
        }
    }

    public void unlock() {
        status = 0;
    }

    /**
     * CAS机制获取锁
     *
     * @param expect
     * @param newValue
     * @return
     */
    boolean compareAndSwapSet(int expect, int newValue) {
        return unsafe.compareAndSwapInt(this, valueOffset, expect, newValue);
    }


}
