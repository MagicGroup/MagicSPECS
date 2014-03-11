/*
 * Original Author:  Daniel Elstner  <daniel.elstner@gmx.net>
 *                   Timeout fix thanks to Bill Tompkins
 * gtk2 port: Bastien Nocera
 * 
 * License: GPL v2
 * Build using:
 * gcc -Wall `pkg-config --cflags --libs gtk+-2.0` -o show-license show-license.c
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <gtk/gtk.h>


static const char license_filename[] = G_DIR_SEPARATOR_S "LICENSE";

enum
{
  EXIT_ACCEPT  = 0,
  EXIT_DECLINE = 1,
  EXIT_NO_X11  = 2
};

static int timeout = 20; /* seconds */


static void scroll_clicked(GtkWidget* widget, void* data)
{
  timeout = 240;
}

static void button_accept_clicked(GtkWidget* widget, void* data)
{
  int* exitcode = (int*) data;

  *exitcode = EXIT_ACCEPT;

  gtk_main_quit();
}

static void update_timer_label(GtkLabel* label)
{
  char* text;

  text = g_strdup_printf("%d seconds until automatic decline", timeout);
  gtk_label_set_text(label, text);
  g_free(text);
}

static int timeout_handler(void* data)
{
  --timeout;

  update_timer_label(GTK_LABEL(data));

  if(timeout > 0)
    return TRUE;

  gtk_main_quit();

  return FALSE;
}

static GtkTextBuffer* load_license_file(const char* prgname)
{
  GtkTextBuffer *txtbuf;
  char*  buffer;
  char* filename, *dir;
  GError *error = NULL;

  dir = g_path_get_dirname(prgname);
  filename = g_build_filename (dir, license_filename, NULL);
  g_free (dir);

  if (g_file_get_contents (filename, &buffer, NULL, &error) == FALSE) {
    g_error("Cannot open file `%s': %s", filename, error->message);
    g_error_free(error);
    g_free(filename);
    exit (1);
  }
  g_free(filename);

  txtbuf = gtk_text_buffer_new(NULL);
  gtk_text_buffer_insert_at_cursor(txtbuf, buffer, -1);
  g_free(buffer);

  return txtbuf;
}

int main(int argc, char** argv)
{
  GtkWidget* window;
  GtkWidget* mainvbox;
  GtkWidget* buttonbox;
  GtkWidget* button_accept;
  GtkWidget* button_decline;
  GtkWidget* table;
  GtkWidget* sw;
  GtkWidget* text;
  GtkTextBuffer* txtbuf;
  int        exitcode;

  if(!gtk_init_check(&argc, &argv))
    exit(EXIT_NO_X11);

  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
  gtk_window_set_default_size(GTK_WINDOW(window), 600, 500);
  gtk_window_set_title(GTK_WINDOW(window), "Macromedia Flash 6 Plugin - End User License Agreement");
  gtk_container_set_border_width(GTK_CONTAINER(window), 0);

  mainvbox = gtk_vbox_new(FALSE, 0);
  gtk_container_add(GTK_CONTAINER(window), mainvbox);

  table = gtk_table_new(1, 2, FALSE);
  gtk_table_set_row_spacing(GTK_TABLE(table), 0, 2);
  gtk_table_set_col_spacing(GTK_TABLE(table), 0, 2);
  gtk_box_pack_start(GTK_BOX(mainvbox), table, TRUE, TRUE, 0);

  /* Create the ScrolledWindow */
  sw = gtk_scrolled_window_new (NULL, NULL);
  gtk_scrolled_window_set_policy (GTK_SCROLLED_WINDOW (sw),
		  GTK_POLICY_NEVER, GTK_POLICY_ALWAYS);

  /* Create the GtkText widget */
  txtbuf = load_license_file(argv[0]);
  text = gtk_text_view_new_with_buffer(txtbuf);
  g_object_unref(txtbuf);
  gtk_text_view_set_editable(GTK_TEXT_VIEW(text), FALSE);
  gtk_text_view_set_wrap_mode (GTK_TEXT_VIEW(text), GTK_WRAP_WORD);
  gtk_container_add(GTK_CONTAINER(sw), text);
  gtk_table_attach(GTK_TABLE(table), sw, 0, 1, 0, 1,
	           GTK_EXPAND | GTK_SHRINK | GTK_FILL,
		   GTK_EXPAND | GTK_SHRINK | GTK_FILL, 0, 0);
  
  gtk_signal_connect(GTK_OBJECT(text), "button_press_event",
                     GTK_SIGNAL_FUNC(&scroll_clicked), 0);

  gtk_signal_connect(GTK_OBJECT(text), "key_press_event",
                     GTK_SIGNAL_FUNC(&scroll_clicked), 0);

  gtk_widget_realize(text);

  if(argc >= 2 && strcmp(argv[1], "--auto") == 0)
  {
    GtkWidget* label;

    label = gtk_label_new(NULL);
    gtk_box_pack_start(GTK_BOX(mainvbox), label, FALSE, TRUE, 5);

    gtk_misc_set_alignment(GTK_MISC(label), 1.0, 0.5);
    gtk_misc_set_padding(GTK_MISC(label), 10, 0);

    update_timer_label(GTK_LABEL(label));

    gtk_timeout_add(1000, &timeout_handler, label);
  }

  buttonbox = gtk_hbutton_box_new();
  gtk_container_set_border_width(GTK_CONTAINER(buttonbox), 5);
  gtk_box_pack_start(GTK_BOX(mainvbox), buttonbox, FALSE, FALSE, 0);

  button_accept  = gtk_button_new_with_label("Accept");
  button_decline = gtk_button_new_with_label("Decline");

  gtk_box_pack_start(GTK_BOX(buttonbox), button_decline, FALSE, FALSE, 0);
  gtk_box_pack_start(GTK_BOX(buttonbox), button_accept,  FALSE, FALSE, 0);

  GTK_WIDGET_SET_FLAGS(button_accept,  GTK_CAN_DEFAULT);
  GTK_WIDGET_SET_FLAGS(button_decline, GTK_CAN_DEFAULT);

  gtk_signal_connect(GTK_OBJECT(window), "destroy",
                     GTK_SIGNAL_FUNC(&gtk_main_quit),
                     NULL);

  gtk_signal_connect(GTK_OBJECT(button_accept), "clicked",
                     GTK_SIGNAL_FUNC(&button_accept_clicked),
                     &exitcode);

  gtk_signal_connect(GTK_OBJECT(button_decline), "clicked",
                     GTK_SIGNAL_FUNC(&gtk_main_quit),
                     NULL);

  gtk_widget_grab_default(button_decline);
  gtk_widget_show_all(window);

  exitcode = EXIT_DECLINE;

  gtk_main();

  exit(exitcode);
  return 0;
}

