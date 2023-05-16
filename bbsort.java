import java.util.Scanner;
import java.util.Arrays;

public class bbsort{
	private static int[] BubbleSort(int[] arr){
		int n = arr.length;
		int x = 0;
		for(int i=0; i<n; i++){
			for(int j=0; j<(n-i-1); j++){
				if(arr[j]>arr[j+1]){
					x = arr[j];
					arr[j] = arr[j+1];
					arr[j+1] = x; 
				}
			}
		}
		return arr;
	}
	private static void print(int[] arr){
		int n = arr.length;
		for(int i=0; i<n; i++){
			System.out.print(arr[i] + ", ");
		}
		System.out.println();
	}

	public static void main(String args[]){
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter size of array: ");
		int n = sc.nextInt();
		int[] array = new int[n];
		System.out.println("Enter elements: ");
		for(int i=0; i<n; i++){
			array[i] = sc.nextInt();
		}
		int[] SortedArr = BubbleSort(array);
		System.out.println("Sorted Array: ");
		print(SortedArr);
	}
}
