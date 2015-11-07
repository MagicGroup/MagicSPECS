%define tarver 18

Name: clit
Summary: Converts Microsoft Reader format eBooks into open format
Summary(zh_CN.UTF-8): 转换 Microsoft Reader 格式的 eBook 为开源格式
Version: 1.8
Release: 4%{?dist}
Source: http://www.convertlit.com/%{name}%{tarver}src.zip
Source1: ltm-0.33.tar.bz2
URL: http://www.convertlit.com/
License: GPL
Group: Publishing
Group(zh_CN.UTF-8): 出版
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This program which allows you to convert Microsoft Reader format eBooks into
open format for use with software or devices which are not directly compatible
with Microsoft's Reader. 

%description -l zh_CN.UTF-8
本程序允许您将 Microsoft Reader 格式的 eBook 转换为开源格式，以便让那些
不兼容 Microsoft 的 Reader 的软件和设备使用。

%prep
%setup -q -a1 -c %{name}-%{version}
perl -p -i -e 's|-O3|\$(RPM_OPT_FLAGS)||g' libtommath-0.33/makefile lib/Makefile clit%{tarver}/Makefile
perl -p -i -e 's|libtommath-0.30|libtommath-0.33||g' clit%{tarver}/Makefile

%build
cd libtommath-0.33
make
cp *.h ../clit%{tarver}
cd ../lib
make %{?_smp_mflags}
cd ../clit%{tarver}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp clit%{tarver}/clit %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.8-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.8-3
- 为 Magic 3.0 重建

* Fri Apr 18 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.8-0.1mgc
- rebuild for Magic Linux 2.1
- 戊子  三月十三

* Thu Sep 06 2007 Patred TheKnight <edupclos@gmail.com> 1.8-1pclos
- Repacked for PCLinuxOS

* Wed Dec 29 2004 Austin Acton <austin@zarb.org> 1.8-1plf
- initial package
