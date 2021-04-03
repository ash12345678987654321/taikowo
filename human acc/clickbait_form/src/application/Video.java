package application;

public class Video {
	private String title,views,likes,dislikes,desc,id;
	private int cb;
	
	public Video(String a,String b,String c,String d,String e,String f,
			String g) {
		title=a;
		views=b;
		likes=c;
		dislikes=d;
		desc=e;
		id=f;
		cb=Integer.parseInt(g);
	}
	
	public String getTitle(){return title;}
	public String getViews(){return views;}
	public String getLikes(){return likes;}
	public String getDislikes(){return dislikes;}
	public String getDesc(){return desc;}
	public String getId(){return id;}
	public int getCb(){return cb;}
}
