Name:           libspectre
Version: 0.2.7
Release: 2%{?dist}
Summary:        A library for rendering PostScript(TM) documents
Summary(zh_CN.UTF-8): 渲染 PostScript(TM) 文档的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://libspectre.freedesktop.org
Source0:        http://libspectre.freedesktop.org/releases/%{name}-%{version}.tar.gz

BuildRequires: ghostscript-devel >= 8.61

%description
%{name} is a small library for rendering PostScript(TM) documents.
It provides a convenient easy to use API for handling and rendering
PostScript documents.

%description -l zh_CN.UTF-8
渲染 PostScript(TM) 文档的库。

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


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS README TODO
%{_libdir}/libspectre.so.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libspectre/
%{_libdir}/libspectre.so
%{_libdir}/pkgconfig/libspectre.pc


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2.7-2
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 0.2.7-1
- 更新到 0.2.7

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.6-6
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 0.2.6-5
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.6-3
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.2.6-2
- rebuild (ghostscript)
- %%files: track sonames (and friends) closer

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Wed Mar  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.4-1
- Update to 0.2.4
- See http://mail.gnome.org/archives/gnome-announce-list/2010-February/msg00059.html

* Fri Jan  8 2010  Marek Kasik <mkasik@redhat.com> - 0.2.3-4
- Correct release number

* Fri Jan  8 2010  Marek Kasik <mkasik@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec  3 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Sun Aug 10 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Sat Feb  9 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.0-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.0-1
- Initial packaging 
