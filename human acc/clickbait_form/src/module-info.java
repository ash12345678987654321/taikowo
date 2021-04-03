module javafx{
	requires javafx.controls;
	requires javafx.fxml;
	requires javafx.graphics;
	exports application;
	opens application;
}