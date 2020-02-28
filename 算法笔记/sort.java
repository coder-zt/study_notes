import java.lang.reflect.Array;
import java.util.Random;

public class sort{
    
    //初始化数据
    static void initData(final int[] data) {
        final Random random = new Random();
        for (int i = 0; i < data.length; i++) {
            data[i] = random.nextInt(data.length);
        }
    }

    // 打印数据
    static void printData(final int data[]) {
        final int linenums = 20;
        for (int i = 0; i < data.length; i++) {
            System.out.print("  " + data[i]);
            if (i % linenums == linenums - 1) {
                System.out.println();
            }
        }
        System.out.println();
    }

    // 冒泡排序
    static void bubbleSort(final int data[]) {
        int temp;
        boolean isExchange = false;
        // 需要进行N趟排序
        for (int i = 0; i < data.length; i++) {
            // 每趟排序的范围是上一趟减一，既每次有一个数据到达自己的位置
            for (int j = 0; j < data.length - i - 1; j++) {
                // 比较前后两个数据，较大者往后交换
                if (data[j] > data[j + 1]) {
                    isExchange = true;
                    temp = data[j];
                    data[j] = data[j + 1];
                    data[j + 1] = temp;
                }
            }
            // 改进：如果本趟未发送交换则代表已经拍好序
            if (!isExchange) {
                break;
            }
            isExchange = false;
        }
    }

    // 快速排序
    static void quickSort(final int data[], int left, int right) {
        int low = left,high = right;
        if (low >= high)
        return;
        int target = data[low];// 初始化指
        // 如果低位小于高位表明，还未找到指标的准确位置
        while (low < high) {
            while (data[high] >= target && low < high) high--;
            if(low >= high){
                break;
            }
            // 交换位置
            data[low] = data[high];
            low++;
            while (data[low] <= target && low < high)low++;
            if(low >= high){
                break;
            }
            // 交换位置
            data[high] = data[low];
            high--;
        }
        //找到target的位置
        data[low] = target;
        quickSort(data, left, low-1);
        quickSort(data, low+1, right);
    }

    public static void main(final String[] args) {
        final int size = 100;
        final int data[] = new int[size];
        initData(data);
        quickSort(data, 0, data.length-1);
        printData(data);
    }
}

