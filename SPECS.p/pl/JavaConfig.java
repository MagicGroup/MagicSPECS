/* JavaConfig - tool for getting paths for current java environment.
 * © 2011  Petr Písař <ppisar@redhat.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

class JavaConfig {
  private static String output = "";


  /*
   * Append text to output with proper padding or terminates if text is null.
   * @param text String to append.
   */
  private static void concatenate(String text) {
    if (text == null) {
      System.exit(2);
    }
    output = (output.equals("") ? ""  : output + " " ) + text;
  }


  /*
   * Show usage message and terminates program with given @exit_code.
   * @param exit_code code to return
   * */
  private static void usage(int exitCode) {
    System.out.print(
        "JavaConfig [OPTIONS]\n" +
        "  --home         Output path to Java home\n" +
        "  --libs-only-L  Output -L linker flags\n" +
        "  --version      Output Java version on first separate line\n"
    );
    System.exit(exitCode);
  }


  /*
   * @Return path to Java home or null in case of error.
   */
  public static String home() {
    return System.getProperty("java.home");
  }


  /*
   * @Return formated libary search path as -L compiler flag,
   * null if error occured.
   * */
  public static String libsOnlyL() {
    String value;
    String architecture = System.getProperty("os.arch");
    String home = home();
    String filesep = System.getProperty("file.separator");
    String paths[];
   
    /* The java.library.path works up to JDK 1.6. */
    if (null == (value = System.getProperty("java.library.path"))) {
      return null;
    }

    /* The java.library.path does not work since JDK 1.7. See
     * <https://bugzilla.redhat.com/show_bug.cgi?id=740762>. */
    if (null == architecture || null == home || null == filesep) {
      return null;
    }
    value = value + ":" +
      home + filesep + "lib" + filesep + architecture + ":" +
      home + filesep + "lib" + filesep + architecture + filesep + "server";


    /* Convert the collon delimited paths to LDFLAGS format */
    paths = value.split(":");

    for (int i = 0; i < paths.length; i++) {
      if (paths[i].equals("")) {
        continue;
      }
      
      if (i == 0) {
        value = "-L" + paths[i];
      } else {
        value = value + " -L" + paths[i];
      }
    }

    return value;
  }


  /*
   * @Return version of Java home or null in case of error.
   */
  public static String version() {
    return System.getProperty("java.version");
  }


  /*
   * Entry point to this class.
   */
  public static void main(String argv[]) {
    if (argv.length < 1) {
      usage(1);
    }

    for (int i = 0; i < argv.length; i++) {
      if (argv[i].equals("--home")) {
          concatenate(home());
      } else if (argv[i].equals("--libs-only-L")) {
          concatenate(libsOnlyL());
      } else if (argv[i].equals("--version")) {
          /* pkg-config prints version on first line */
          String version = version();
          if (null == version) {
            System.exit(2);
          }
          System.out.println(version);
      } else {
          usage(1);
      }
    }

    if (!output.equals("")) {
      System.out.println(output);
    }
    System.exit(0);
  }
}
