package org.jarvis.test;

import org.jarvis.utils.CASLock;

/**
 * @author tennyson
 * @date 2021/4/23-12:55
 */
public class CASLockTest {
    private CASLock casLock = new CASLock();
    int k = 0;
    private byte[] l = new byte[1];
    Thread t1;
    Thread t2;

    public static void main(String[] args) throws InterruptedException {
        CASLockTest test = new CASLockTest();
        test.concurrentRun();
    }

    public void concurrentRun() throws InterruptedException {
        t1 = new Thread() {
            @Override
            public void run() {
                sum();
            }
        };

        t2 = new Thread() {
            @Override
            public void run() {
                sum();
            }
        };

        t1.start();
        t2.start();
        //阻塞
        t1.join();
        t2.join();
        //2w
        System.out.println(k);
    }

    public void sum() {
        /**
         * 锁 对象当中的一个标识
         * 加锁：就是去改变这个对象的标识的值
         * 加锁成功：让方法正常返回
         * 加锁失败：让失败的这个线程 死循环 阻塞
         */
        casLock.lock();
        //业内一般叫做锁对象
        //synchronized究竟改变了l对象的什么东西
//        synchronized (l) {

        for (int i = 0; i < 10000; i++) {
            k = k + 1;
        }
//        }

        casLock.unlock();

    }
}
