Name:           libgee06
Version:        0.6.1
Release:        6%{?dist}
Summary:        GObject collection library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://live.gnome.org/Libgee
#VCS:           git:git://git.gnome.org/libgee
Source0:        http://download.gnome.org/sources/libgee/0.6/libgee-%{version}.tar.bz2

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
# Bootstrap requirements
BuildRequires:  autoconf automake libtool
BuildRequires:  vala

%description
libgee is a collection library providing GObject-based interfaces and
classes for commonly used data structures.

libgee provides the following interfaces:

* Iterable
  * Collection
    * List
    * Set
    * MultiSet
    * Queue
      * Deque
* Iterator
* Map
* MultiMap

The ArrayList, HashSet, HashMap, HashMultiSet, HashMultiMap,
LinkedList, PriorityQueue, TreeSet, TreeMap, TreeMultiSet, and
TreeMultiMap classes provide a reasonable sample implementation of
those interfaces. In addition, a set of abstract classes are provided
to ease the implementation of new collections.

Around that, the API provide means to retrieve read-only views,
efficient sort algorithms, simple, bi-directional or index-based
mutable iterators depending on the collection type.

libgee is written in Vala and can be used like any GObject-based C library.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libgee-%{version}
# ChangeLog not UTF8
iconv -f iso88591 -t utf8 ChangeLog -o ChangeLog.new
touch -r ChangeLog ChangeLog.new
mv ChangeLog.new ChangeLog


%build
(if ! test -x configure; then
    NOCONFIGURE=1 ./autogen.sh;
    CONFIGFLAGS=--enable-gtk-doc;
 fi;
 %configure --disable-static $CONFIGFLAGS
)
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Gee-1.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gee-1.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gee-1.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gee-1.0.vapi


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.6.1-6
- 为 Magic 3.0 重建

* Fri Sep  9 2011 Michel Salim <salimma@fedoraproject.org> - 0.6.1-5
- spec cleanup

* Thu Sep  8 2011 Michel Salim <salimma@fedoraproject.org> - 0.6.1-4
- libgee06, based on the last 0.6.x series libgee for F-16

* Thu Sep  1 2011 Michel Salim <salimma@fedoraproject.org> - 0.6.1-3
- Move typelib file to main package (# 735081)
- Re-enable unit tests on all Fedora releases
- -devel subpackage no longer depends on vala and gobject-introspection-devel

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Sun Dec 12 2010 Michel Salim <salimma@fedoraproject.org> - 0.6.0-2
- Update spec to support snapshot builds (# 609294)

* Thu Oct 28 2010 Michel Salim <salimma@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Wed Sep 29 2010 jkeating - 0.5.3-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Michel Salim <salimma@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3
- Rebuild against newer gobject-introspection

* Wed Aug 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.5.2-2
- Add BR on gobject-introspection-devel.

* Wed Aug 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2.
- Remove buildroot & clean section. No longer needed.

* Thu Jun 17 2010 Michel Salim <salimma@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Sat Oct  3 2009 Michel Salim <salimma@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Thu Aug 20 2009 Michel Salim <salimma@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  2 2009 Michel Salim <salimma@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.4-2
- Run unit tests only on releases with glib2 >= 2.16

* Sat Dec 13 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4

* Mon Aug 25 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.1-3
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Michel Salim <michel.sylvan@gmail.com> - 0.1.1-2
- Move pkgconfig requirement to -devel subpackage

* Sat Jan 26 2008 Michel Salim <michel.sylvan@gmail.com> - 0.1.1-1
- Initial Fedora package
