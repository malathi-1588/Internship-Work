import java.util.*;

public class search{
	private static void search(int x, int[] arr){
		int n = arr.length;
		for(int i=0; i<n; i++){
			if(arr[i]==x){
				System.out.printf("Element found at position %d", i+1);
				break;
			}
		}
	}

	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter size of array: ");
		int n = sc.nextInt();
		int[] array = new int[n];
		System.out.println("Enter elements: ");
		for(int i=0; i<n; i++){
			array[i] = sc.nextInt();
		}
		System.out.println("Enter element to search: ");
		int x = sc.nextInt();
		search(x, array);
	}
}