package application;

import javafx.fxml.FXML;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

import javafx.event.ActionEvent;
import javafx.scene.control.Button;
import javafx.scene.control.Label;

import javafx.scene.control.TextArea;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

public class SampleController {
	@FXML
	private ImageView img;
	@FXML
	private TextArea desc;
	@FXML
	private Label title;
	@FXML
	private Label views;
	@FXML
	private Label likes;
	@FXML
	private Label dislikes;
	@FXML
	private Button btn1;
	@FXML 
	private Button btn2;
	
	private ArrayList<Video> videos=new ArrayList<Video>();
	private int index=0;
	
	private FileWriter writer; 
	
	private void populate() {
		if (index==videos.size()) {
			btn1.setDisable(true);
			btn2.setDisable(true);
			
			try {
				writer.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			return;
		}
		
		Video curr=videos.get(index);
		
		img.setImage(new Image("file:../../thumbs/"+curr.getId()+".jpg"));
		desc.setText(curr.getDesc());
		title.setText(curr.getTitle());
		views.setText(curr.getViews());
		likes.setText(curr.getLikes());
		dislikes.setText(curr.getDislikes());
	}
	
	@FXML
    public void initialize() {
        System.out.println("initialize");
        
        Scanner scanner;
		try {
			scanner = new Scanner(new File("../metadata.txt"));
			scanner.useDelimiter("\0");
	        
			while(scanner.hasNext()){
				videos.add(new Video(
						scanner.next(),
						scanner.next(),
						scanner.next(),
						scanner.next(),
						scanner.next(),
						scanner.next(),
						scanner.next()
				));
				System.out.println(videos.get(videos.size()-1).getTitle());
			}
			
			writer=new FileWriter("../results.txt");
		} catch (Exception e) { //laziness
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		populate();
    }

	// Event Listener on Button.onAction
	@FXML
	public void clickbait(ActionEvent event) {
		System.out.println("clickbait");
		
		try {
			writer.write("1\n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		index++;
		populate();
	}
	// Event Listener on Button.onAction
	@FXML
	public void not_clickbait(ActionEvent event) {
		System.out.println("not clickbait");
		
		try {
			writer.write("0\n");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		index++;
		populate();
	}
}
