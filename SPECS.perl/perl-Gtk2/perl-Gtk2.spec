#
# Rebuild option:
#
#   --with testsuite         - run the test suite (requires X)
#

# We need to manually generate the Provides here, here's the best way I know of:
# for i in `grep -r "PACKAGE = " * | cut -d " " -f 3 | cut -f 1`; do printf "Provides: perl($i)\n" &>>provides.txt; done
# cat provides.txt | sort -n | uniq

Name:           perl-Gtk2
Version:	1.2496
Release:	1%{?dist}
Summary:        Perl interface to the 2.x series of the Gimp Toolkit library
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://search.cpan.org/dist/Gtk2/
Source0:        http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/Gtk2-%{version}.tar.gz
BuildRequires:  perl >= 2:5.8.0
BuildRequires:  gtk2-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Depends), perl(ExtUtils::PkgConfig)
BuildRequires:  perl(Glib) >= 1.240
BuildRequires:	perl(Pango) >= 1.220
BuildRequires:  perl(Glib::MakeHelper)
BuildRequires:  perl(Cairo) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Glib) >= 1.240
Requires:       perl(Cairo) >= 1.00
Requires:       perl(Pango) >= 1.220
# Be sure to update this list on any upstream change
Provides: perl(Gtk2)
Provides: perl(Gtk2::AboutDialog)
Provides: perl(Gtk2::AccelGroup)
Provides: perl(Gtk2::AccelLabel)
Provides: perl(Gtk2::AccelMap)
Provides: perl(Gtk2::Action)
Provides: perl(Gtk2::ActionGroup)
Provides: perl(Gtk2::Activatable)
Provides: perl(Gtk2::Adjustment)
Provides: perl(Gtk2::Alignment)
Provides: perl(Gtk2::Arrow)
Provides: perl(Gtk2::AspectFrame)
Provides: perl(Gtk2::Assistant)
Provides: perl(Gtk2::Bin)
Provides: perl(Gtk2::BindingSet)
Provides: perl(Gtk2::Box)
Provides: perl(Gtk2::Buildable)
Provides: perl(Gtk2::Builder)
Provides: perl(Gtk2::Button)
Provides: perl(Gtk2::ButtonBox)
Provides: perl(Gtk2::Calendar)
Provides: perl(Gtk2::CellEditable)
Provides: perl(Gtk2::CellLayout)
Provides: perl(Gtk2::CellRenderer)
Provides: perl(Gtk2::CellRendererAccel)
Provides: perl(Gtk2::CellRendererCombo)
Provides: perl(Gtk2::CellRendererPixbuf)
Provides: perl(Gtk2::CellRendererProgress)
Provides: perl(Gtk2::CellRendererSpin)
Provides: perl(Gtk2::CellRendererSpinner)
Provides: perl(Gtk2::CellRendererText)
Provides: perl(Gtk2::CellRendererToggle)
Provides: perl(Gtk2::CellView)
Provides: perl(Gtk2::CheckButton)
Provides: perl(Gtk2::CheckMenuItem)
Provides: perl(Gtk2::Clipboard)
Provides: perl(Gtk2::ColorButton)
Provides: perl(Gtk2::ColorSelection)
Provides: perl(Gtk2::ColorSelectionDialog)
Provides: perl(Gtk2::Combo)
Provides: perl(Gtk2::ComboBox)
Provides: perl(Gtk2::ComboBoxEntry)
Provides: perl(Gtk2::Container)
Provides: perl(Gtk2::Curve)
Provides: perl(Gtk2::Dialog)
Provides: perl(Gtk2::Dnd)
Provides: perl(Gtk2::DrawingArea)
Provides: perl(Gtk2::Editable)
Provides: perl(Gtk2::Entry)
Provides: perl(Gtk2::EntryBuffer)
Provides: perl(Gtk2::EntryCompletion)
Provides: perl(Gtk2::EventBox)
Provides: perl(Gtk2::Expander)
Provides: perl(Gtk2::FileChooser)
Provides: perl(Gtk2::FileChooserButton)
Provides: perl(Gtk2::FileChooserDialog)
Provides: perl(Gtk2::FileChooserWidget)
Provides: perl(Gtk2::FileFilter)
Provides: perl(Gtk2::FileSelection)
Provides: perl(Gtk2::Fixed)
Provides: perl(Gtk2::FontButton)
Provides: perl(Gtk2::FontSelection)
Provides: perl(Gtk2::Frame)
Provides: perl(Gtk2::GammaCurve)
Provides: perl(Gtk2::GC)
Provides: perl(Gtk2::Gdk)
Provides: perl(Gtk2::Gdk::Cairo)
Provides: perl(Gtk2::Gdk::Color)
Provides: perl(Gtk2::Gdk::Cursor)
Provides: perl(Gtk2::Gdk::Device)
Provides: perl(Gtk2::Gdk::Display)
Provides: perl(Gtk2::Gdk::DisplayManager)
Provides: perl(Gtk2::Gdk::Dnd)
Provides: perl(Gtk2::Gdk::Drawable)
Provides: perl(Gtk2::Gdk::Event)
Provides: perl(Gtk2::Gdk::GC)
Provides: perl(Gtk2::Gdk::Image)
Provides: perl(Gtk2::Gdk::Keys)
Provides: perl(Gtk2::Gdk::Pango)
Provides: perl(Gtk2::Gdk::Pixbuf)
Provides: perl(Gtk2::Gdk::PixbufLoader)
Provides: perl(Gtk2::Gdk::PixbufSimpleAnim)
Provides: perl(Gtk2::Gdk::Pixmap)
Provides: perl(Gtk2::Gdk::Property)
Provides: perl(Gtk2::Gdk::Region)
Provides: perl(Gtk2::Gdk::Rgb)
Provides: perl(Gtk2::Gdk::Screen)
Provides: perl(Gtk2::Gdk::Selection)
Provides: perl(Gtk2::Gdk::Types)
Provides: perl(Gtk2::Gdk::Visual)
Provides: perl(Gtk2::Gdk::Window)
Provides: perl(Gtk2::Gdk::X11)
Provides: perl(Gtk2::HandleBox)
Provides: perl(Gtk2::HBox)
Provides: perl(Gtk2::HButtonBox)
Provides: perl(Gtk2::HPaned)
Provides: perl(Gtk2::HRuler)
Provides: perl(Gtk2::HScale)
Provides: perl(Gtk2::HScrollbar)
Provides: perl(Gtk2::HSeparator)
Provides: perl(Gtk2::HSV)
Provides: perl(Gtk2::IconFactory)
Provides: perl(Gtk2::IconTheme)
Provides: perl(Gtk2::IconView)
Provides: perl(Gtk2::Image)
Provides: perl(Gtk2::ImageMenuItem)
Provides: perl(Gtk2::IMContext)
Provides: perl(Gtk2::IMContextSimple)
Provides: perl(Gtk2::IMMultiContext)
Provides: perl(Gtk2::InfoBar)
Provides: perl(Gtk2::InputDialog)
Provides: perl(Gtk2::Invisible)
Provides: perl(Gtk2::Item)
Provides: perl(Gtk2::ItemFactory)
Provides: perl(Gtk2::Label)
Provides: perl(Gtk2::Layout)
Provides: perl(Gtk2::LinkButton)
Provides: perl(Gtk2::List)
Provides: perl(Gtk2::ListItem)
Provides: perl(Gtk2::ListStore)
Provides: perl(Gtk2::Menu)
Provides: perl(Gtk2::MenuBar)
Provides: perl(Gtk2::MenuItem)
Provides: perl(Gtk2::MenuShell)
Provides: perl(Gtk2::MenuToolButton)
Provides: perl(Gtk2::MessageDialog)
Provides: perl(Gtk2::Misc)
Provides: perl(Gtk2::Notebook)
Provides: perl(Gtk2::Object)
Provides: perl(Gtk2::OffscreenWindow)
Provides: perl(Gtk2::OptionMenu)
Provides: perl(Gtk2::Orientable)
Provides: perl(Gtk2::PageSetup)
Provides: perl(Gtk2::Paned)
Provides: perl(Gtk2::PaperSize)
Provides: perl(Gtk2::Plug)
Provides: perl(Gtk2::PrintContext)
Provides: perl(Gtk2::PrintOperation)
Provides: perl(Gtk2::PrintOperationPreview)
Provides: perl(Gtk2::PrintSettings)
Provides: perl(Gtk2::ProgressBar)
Provides: perl(Gtk2::RadioAction)
Provides: perl(Gtk2::RadioButton)
Provides: perl(Gtk2::RadioMenuItem)
Provides: perl(Gtk2::RadioToolButton)
Provides: perl(Gtk2::Range)
Provides: perl(Gtk2::Rc)
Provides: perl(Gtk2::RecentAction)
Provides: perl(Gtk2::RecentChooser)
Provides: perl(Gtk2::RecentChooserDialog)
Provides: perl(Gtk2::RecentChooserMenu)
Provides: perl(Gtk2::RecentChooserWidget)
Provides: perl(Gtk2::RecentFilter)
Provides: perl(Gtk2::RecentManager)
Provides: perl(Gtk2::Ruler)
Provides: perl(Gtk2::Scale)
Provides: perl(Gtk2::ScaleButton)
Provides: perl(Gtk2::ScrolledWindow)
Provides: perl(Gtk2::Selection)
Provides: perl(Gtk2::SeparatorMenuItem)
Provides: perl(Gtk2::SeparatorToolItem)
Provides: perl(Gtk2::Show)
Provides: perl(Gtk2::SizeGroup)
Provides: perl(Gtk2::Socket)
Provides: perl(Gtk2::SpinButton)
Provides: perl(Gtk2::Spinner)
Provides: perl(Gtk2::Statusbar)
Provides: perl(Gtk2::StatusIcon)
Provides: perl(Gtk2::Stock)
Provides: perl(Gtk2::Style)
Provides: perl(Gtk2::Table)
Provides: perl(Gtk2::TearoffMenuItem)
Provides: perl(Gtk2::TextBuffer)
Provides: perl(Gtk2::TextBufferRichText)
Provides: perl(Gtk2::TextChildAnchor)
Provides: perl(Gtk2::TextIter)
Provides: perl(Gtk2::TextMark)
Provides: perl(Gtk2::TextTag)
Provides: perl(Gtk2::TextTagTable)
Provides: perl(Gtk2::TextView)
Provides: perl(Gtk2::ToggleAction)
Provides: perl(Gtk2::ToggleButton)
Provides: perl(Gtk2::ToggleToolButton)
Provides: perl(Gtk2::Toolbar)
Provides: perl(Gtk2::ToolButton)
Provides: perl(Gtk2::ToolItem)
Provides: perl(Gtk2::ToolItemGroup)
Provides: perl(Gtk2::ToolPalette)
Provides: perl(Gtk2::ToolShell)
Provides: perl(Gtk2::Tooltip)
Provides: perl(Gtk2::Tooltips)
Provides: perl(Gtk2::TreeDnd)
Provides: perl(Gtk2::TreeModel)
Provides: perl(Gtk2::TreeModelFilter)
Provides: perl(Gtk2::TreeModelSort)
Provides: perl(Gtk2::TreeSelection)
Provides: perl(Gtk2::TreeSortable)
Provides: perl(Gtk2::TreeStore)
Provides: perl(Gtk2::TreeView)
Provides: perl(Gtk2::TreeViewColumn)
Provides: perl(Gtk2::UIManager)
Provides: perl(Gtk2::VBox)
Provides: perl(Gtk2::VButtonBox)
Provides: perl(Gtk2::Viewport)
Provides: perl(Gtk2::VolumeButton)
Provides: perl(Gtk2::VPaned)
Provides: perl(Gtk2::VRuler)
Provides: perl(Gtk2::VScale)
Provides: perl(Gtk2::VScrollbar)
Provides: perl(Gtk2::VSeparator)
Provides: perl(Gtk2::Widget)
Provides: perl(Gtk2::Window)

%global __requires_exclude perl\\(Glib\\)|perl\\(Test::

%description
This module allows you to write Gtk+ graphical user interfaces in a
perlish and object-oriented way, freeing you from the casting and
memory management in C, yet remaining very close in spirit to original
API.  Find out more about Gtk+ at http://www.gtk.org.

%prep
%setup -q -n Gtk2-%{version}

# iconv -f iso-8859-1 -t utf-8 -o pm/Helper.pm{.utf8,}
# mv pm/Helper.pm{.utf8,}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%{?_with_testsuite:make test}

%files
%doc AUTHORS ChangeLog.pre-git LICENSE NEWS README TODO
%doc examples/ gtk-demo/
%{perl_vendorarch}/auto/Gtk2/
%{perl_vendorarch}/Gtk2*
%{_mandir}/man3/*.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.2496-1
- 更新到 1.2496

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.246-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.246-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.246-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.246-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.246-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.246-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.246-2
- 为 Magic 3.0 重建

* Mon Dec 10 2012 Tom Callaway <spot@fedoraproject.org> - 1.246-1
- update to 1.246

* Fri Nov 30 2012 Tom Callaway <spot@fedoraproject.org> - 1.245-2
- add manual provides

* Wed Aug  8 2012 Tom Callaway <spot@fedoraproject.org> - 1.245-1
- update to 1.245

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.243-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.243-2
- Perl 5.16 rebuild

* Tue May  1 2012 Tom Callaway <spot@fedoraproject.org> - 1.243-1
- update to 1.243

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.241-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Tom Callaway <spot@fedoraproject.org> - 1.241-1
- update to 1.241

* Thu Oct 20 2011 Tom Callaway <spot@fedoraproject.org> - 1.240-1
- update to 1.240

* Tue Aug 30 2011 Tom Callaway <spot@fedoraproject.org> - 1.224-2
- filter out bogus Requires on Test::More

* Wed Aug  3 2011 Tom Callaway <spot@fedoraproject.org> - 1.224-1
- update to 1.224

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.223-3
- Perl mass rebuild

* Thu Apr 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.223-2
- add provides, which should fix gcstar. They must be provided by this
 package.
- use new filtering of requires. Filter of provides not needed anymore.

* Tue Mar 29 2011 Tom Callaway <spot@fedoraproject.org> - 1.223-1
- update to 1.223

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.203-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.203-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.203-6
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.203-4
- add perl_default_filter to drop "Gtk2.so" provides

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.203-4
- rebuild against perl 5.10.1

* Thu Jul 30 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.203-3
- Fix mass rebuild breakdown: 
  Add BR: perl(ExtUtils::MakeMaker), perl(Glib::MakeHelper).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.203-1
- update to 1.203

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.162-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.162-3
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.162-1
- Update to 1.162

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.144-1
- Update to 1.144.

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.143-1
- Update to 1.143.

* Sun Jan 21 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.142-1
- Update to 1.142.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.141-1
- Update to 1.141.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.140-1
- Update to 1.140.

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.122-1
- Update to 1.122.

* Mon May  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.121-2
- Requires perl(Cairo)  (distro >= FC-5).

* Tue Apr 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.121-1
- Update to 1.121.

* Tue Mar 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.120-1
- Update to 1.120.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.104-1
- Update to 1.104.
- Requires perl(Glib) >= 1.105 (1.104 had problems with perl 5.8.8).

* Thu Jan 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.103-1
- Update to 1.103.
- Converted the Gtk2::Helper man page to utf8 (#177802).
- Provides list: filtered out perl(main) (#177802).

* Wed Nov 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.102-1
- Update to 1.102.

* Thu Oct  6 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.101-1
- Update to 1.101.

* Thu Sep  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.100-1
- Update to 1.100.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.083-1
- Update to 1.083.

* Mon Jun 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.082-1
- Update to 1.082.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Mar 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.080-2
- Use perl-Glib for versioning control (patch by Ville Skyttä).

* Tue Mar  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.080-1
- Update to 1.080.

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.062-1
- Update to 1.062.

* Mon Oct 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.061-0.fdr.2
- Removed irrelevant or duplicated documentation files.
- Description simplified (as suggested by Ville Skyttä).

* Tue Oct  5 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.061-0.fdr.1
- Update to 1.061.

* Tue Oct  5 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.043-0.fdr.2
- make test commented: needs X.

* Sun Jul 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.043-0.fdr.1
- First build.
