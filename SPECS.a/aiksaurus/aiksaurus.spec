Name: 		aiksaurus
Version: 	1.2.1
Release: 	25%{?dist}
Summary: 	An English-language thesaurus library
Summary(zh_CN.UTF-8): 英语同义词库

Epoch: 		1
Group: 		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License: 	GPLv2+
URL: 		http://aiksaurus.sourceforge.net/
Source0: 	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.png
Source2: 	%{name}.desktop
Patch0:		%{name}-1.2.1-gcc43.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: 	gtk2-devel
BuildRequires:	desktop-file-utils

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils


%description
Aiksaurus is an English-language thesaurus library that can be 
embedded in word processors, email composers, and other authoring
software to provide thesaurus capabilities.  A basic command line 
thesaurus program is also included.

%description -l zh_CN.UTF-8
英语同义词库。

%package devel
Requires: 	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary: 	Files for developing with aiksaurus
Summary(zh_CN.UTF-8): %name 的开发包
Group: 		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
                                                                               
%description devel
Includes and definitions for developing with aiksaurus.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%package gtk
Requires: 	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary: 	A GTK+ frontend to aiksaurus
Summary(zh_CN.UTF-8): %name 的 GTK+ 前端
Group: 		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库

%description gtk
AiksaurusGTK is a GTK+ interface to the Aiksaurus library.  
It provides an attractive thesaurus interface, and can be embedded
in GTK+ projects, notably AbiWord.  A standalone thesaurus program
is also provided.

%description gtk -l zh_CN.UTF-8
%name 的 GTK+ 前端。

%package gtk-devel
Requires: 	%{name}-gtk = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: 	gtk2-devel
Summary: 	Files for developing with aiksaurus-gtk
Summary(zh_CN.UTF-8): %name GTK+ 前端的开发包
Group: 		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
                                                                               
%description gtk-devel
gtk includes and definitions for developing with aiksaurus.

%description gtk-devel -l zh_CN.UTF-8
%name GTK+ 前端的开发包。

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
magic_rpm_clean.sh
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# Add the desktop icon.
%{__install} -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png

# Add desktop file.
desktop-file-install --vendor magic                    \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        %{SOURCE2}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /usr/sbin/ldconfig


%postun -p /usr/sbin/ldconfig


%post gtk
/usr/sbin/ldconfig
update-desktop-database &> /dev/null ||:


%postun gtk
/usr/sbin/ldconfig
update-desktop-database &> /dev/null ||:


%files
%defattr(-, root, root)
%doc ChangeLog README COPYING AUTHORS
%{_bindir}/%{name}
%{_bindir}/caiksaurus
%{_libdir}/*Aiksaurus-*.so.*
%{_datadir}/%{name}/


%files devel
%defattr(-, root, root)
%dir %{_includedir}/Aiksaurus
%{_includedir}/Aiksaurus/Aiksaurus.h
%{_includedir}/Aiksaurus/AiksaurusC.h
%{_libdir}/*Aiksaurus.so
%{_libdir}/pkgconfig/%{name}-1.0.pc


%files gtk
%defattr(-, root, root)
%{_bindir}/gaiksaurus
%{_libdir}/*GTK*.so.*
%{_datadir}/applications/magic-%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


%files gtk-devel
%defattr(-, root, root)
%{_includedir}/Aiksaurus/AiksaurusGTK*.h
%{_libdir}/*GTK*.so
%{_libdir}/pkgconfig/gaiksaurus-1.0.pc


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1:1.2.1-25
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1:1.2.1-23
- 为 Magic 3.0 重建
