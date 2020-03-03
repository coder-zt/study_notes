import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

class myThread extends Thread {
    int count = 10;
    String name;

    myThread(String name) {
        super("super-" + name);
        this.name = name;
    }

    @Override
    public void run() {
        // TODO Auto-generated method stub
        super.run();
        while (0 < count--) {
            System.out.println(super.currentThread().getName() + "正在工作。。。");
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }
}

class myRunnableThread implements Runnable {
    String name;
    int count = 10;
    Thread t;

    myRunnableThread(String name) {
        this.name = name;

    }

    public void run() {
        // TODO Auto-generated method stub
        while (0 < count--) {
            System.out.println(name + "正在工作。。。");
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    public void start() {
        if (t == null) {
            t = new Thread(this);
            t.start();
        }

    }

}

class myCallableThread implements Callable<String> {

    @Override
    public String call() throws Exception {
        // TODO Auto-generated method stub
        if (Thread.currentThread().getName() == "张滔"){
            
            return "李林璐的滔姐姐";
        }

        if (Thread.currentThread().getName() == "李林璐"){
            Thread.sleep(5000);
            return "张滔的小姐姐";
        }
           
        return null;
    }

}

public class ThreadTest {

    public static void main(String[] args) {
        // myThread t1 = new myThread("张滔");
        // t1.start();
        // myThread t2 = new myThread("李林璐");
        // t2.start();

        // myRunnableThread t1 = new myRunnableThread("张滔");
        // t1.start();
        // myRunnableThread t2 = new myRunnableThread("李林璐");
        // t2.start();

        myCallableThread t1 = new myCallableThread();
        FutureTask fut1 = new FutureTask<String>(t1);
        // myCallableThread t2 = new myCallableThread();
        FutureTask fut2 = new FutureTask<String>(t1);
        new Thread(fut1, "李林璐").start();
        new Thread(fut2, "张滔").start();
        try {
            System.out.println(fut2.get());
            System.out.println(fut1.get());

        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (ExecutionException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}