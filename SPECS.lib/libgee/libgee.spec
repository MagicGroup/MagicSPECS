Name:           libgee
Version:	0.18.0
Release:        2%{?dist}
Summary:        GObject collection library
Summary(zh_CN.UTF-8): GObject 收集库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://live.gnome.org/Libgee
#VCS:           git:git://git.gnome.org/libgee
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/libgee/%{majorver}/libgee-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
# Bootstrap requirements
BuildRequires:  autoconf automake libtool
BuildRequires:  vala

%description
libgee is a collection library providing GObject-based interfaces and
classes for commonly used data structures.

* Traversable
  o Iterable
    + Collection
      - List
        * BidirList
      - Set
        * SortedSet
          o BidirSortedSet
      - MultiSet
      - Queue
        * Deque
    + Map
      - SortedMap
        * BidirSortedMap
  o Iterator
    + BidirIterator
      - BidirListIterator
    + ListIterator
      - BidirListIterator
* MultiMap

The ArrayList, ArrauQueue, ConcurrentLinkedList, ConcurrentSet, HashSet,
HashMap, HashMultiSet, HashMultiMap, LinkedList, PriorityQueue, TreeSet,
TreeMap, TreeMultiSet, and TreeMultiMap classes provide a reasonable sample
implementation of those interfaces. In addition, a set of abstract
classes are provided to ease the implementation of new collections.

Around that, the API provide means to retrieve read-only views,
efficient sort algorithms, simple, bi-directional or index-based mutable
iterators depending on the collection type.

Libgee is written in Vala and can be used like any GObject-based C
library. It's planned to provide bindings for further languages.

%description -l zh_CN.UTF-8
GObject 集合库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
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
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Gee-0.8.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gee-0.8.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gee-0.8.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gee-0.8.vapi


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.18.0-2
- 更新到 0.18.0

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 0.15.3-1
- 更新到 0.15.3

* Mon Apr 15 2013 Michel Salim <salimma@fedoraproject.org> - 0.10.1-1
- Update to 0.10.1

* Tue Mar 26 2013 Michel Salim <salimma@fedoraproject.org> - 0.10.0-1
- Update to 0.10.0

* Fri Mar  8 2013 Matthias Clasen <mclasen@redhat.com> - 0.8.5-1
- Update to 0.8.5

* Thu Feb 21 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4.
- Drop unnecessary define file attr.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Michel Salim <salimma@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2
- Drop s390x patch, no longer needed

* Tue Oct 16 2012 Michel Salim <salimma@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Wed Sep 26 2012 Michel Salim <salimma@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0

* Wed Sep  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.7.90-1
- Update to 0.7.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Michel Salim <salimma@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2

* Thu Jan 12 2012 Dan Horák <dan[at]danny.cz> - 0.7.1-2
- fix build, see patch comment for details

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Thu Sep  1 2011 Michel Salim <salimma@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

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
