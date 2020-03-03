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
            // 改进：如果本趟未发送交换则代表已经排好序
            if (!isExchange) {
                break;
            }
            isExchange = false;
        }
    }

    // 分治算法思想->求无序数组中的中位数
    static int findMiddle( int data[], int left, int right) {
        int low = left,high = right;
        int target = low;// 初始化指
        int temp;
        if (low < high){
            // 如果低位小于高位表明，还未找到指标的准确位置
            while (low < high) {
                //分别在两端查找小于、大于target的位置
                while (data[high] >= data[target] && low < high) high--;
                while (data[low] <= data[target] && low < high)low++;
                if(low < high){
                    //交换高低位数据
                    temp = data[low];
                    data[low]= data[high];
                    data[high] = temp;
                }
            }
            //找到data[target]的位置
            temp = data[low];
            data[low] = data[target];
            data[target] = temp;
            
        }
        if(low == data.length/2){
            return data[low];
        }
        else if(low < data.length/2){
            return findMiddle(data, low+1, right);
        }else{
            return findMiddle(data, left, low-1);
         }
    }

    // 快速排序
    static void quickSort(final int data[], int left, int right) {
        int low = left,high = right;
        int target = low;// 初始化指
        int temp;
        if (low < high){
            // 如果低位小于高位表明，还未找到指标的准确位置
            while (low < high) {
                //分别在两端查找小于、大于target的位置
                while (data[high] >= data[target] && low < high) high--;
                while (data[low] <= data[target] && low < high)low++;
                if(low < high){
                    //交换高低位数据
                    temp = data[low];
                    data[low]= data[high];
                    data[high] = temp;
                }
            }
            //找到data[target]的位置
            temp = data[low];
            data[low] = data[target];
            data[target] = temp;
            quickSort(data, left, low-1);
            quickSort(data, low+1, right);
        } 
    }

    //直接插入排序
    public static void InsertSort(int data[]){
        int target;//记录当前待插入元素的值
        //从第2个元开始向有序部分插入
        for(int i=1;i<data.length;i++){
            target = data[i];
            for(int j = i-1; j>=0;j--){
                if(data[j]>target){//若大于target则后移
                    data[j+1] = data[j];
                }else{
                    data[j] = target;
                    break;
                }
                if(j == 0){
                    data[j] = target;
                }
            }
        }
    }

    public static void main(final String[] args) {
        final int size = 100;
        final int data[] = new int[size];
        initData(data);
        InsertSort(data);
        // System.out.println("中位数==" + findMiddle(data, 0, data.length-1));
        printData(data);
    }
}

