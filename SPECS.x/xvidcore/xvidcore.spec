Summary: Free reimplementation of the OpenDivX video codec
Name: xvidcore
Version: 1.3.2
Release: 2%{?dist}
License: XviD
Group: System Environment/Libraries
Source0: http://downloads.xvid.org/downloads/%{name}-%{version}.tar.gz
URL: http://www.xvid.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: /sbin/ldconfig
%ifarch %ix86 ia64
BuildRequires: nasm
%endif
Obsoletes: xvidcore-static <= %{eversion}

%description
Free reimplementation of the OpenDivX video codec. You can play OpenDivX
and DivX4 videos with it, as well as encode compatible files.

%package libs
Summary: Shared libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的共享库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description libs
Shared libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的动态共享库。

%package static
Summary: Static libs for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package devel
Summary: Devel files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Devel files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。


%prep
%setup -q -n %{name}

%build
cd build/generic
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build/generic
make install DESTDIR=%{buildroot}
/sbin/ldconfig -n %{buildroot}%{_libdir}
cd %{buildroot}%{_libdir}
for x in `ls *.so.* | grep '\.so\.[^.]*$'`; do
  chmod 0755 $x
  ln -s $x `echo $x | sed -e's,\.so.*,.so,'`
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README* ChangeLog AUTHORS TODO
%doc CodingStyle doc examples

%files libs
%defattr(-,root,root,-)
%{_libdir}/libxvidcore.so.*

%files static
%defattr(-,root,root,-)
%{_libdir}/libxvidcore.a

%files devel
%defattr(-,root,root,-)
%{_libdir}/libxvidcore.so
%{_includedir}/xvid.h

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.3.2-2
- 为 Magic 3.0 重建


