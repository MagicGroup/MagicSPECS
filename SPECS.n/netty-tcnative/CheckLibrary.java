import org.apache.tomcat.jni.Library;

public class CheckLibrary {

  public static void main(String[] a) throws Exception{
   Library.initialize(null);
  }
}
