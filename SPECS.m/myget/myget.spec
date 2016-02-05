%define version  0.1.2
%define subver   20050921

Name: myget
Summary: A download accelerator for GNU/Linux
Summary(zh_CN.UTF-8): GNU/Linux下的下载加速器
Version: %{version}
Release: 6%{?dist}
License: GPL
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Url: http://myget.sourceforge.net
Source: http://myget.sourceforge.net/release/%{name}-%{version}.tar.gz
Patch2: myget-0.1.2-gcc5.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{subver}-%{release}-buildroot
Packager: kde <jack@linux.net.cn>, Magic Group
Prefix: %{_prefix}

%description
Myget is a download accelerator for GNU/Linux.

%description -l zh_CN.UTF-8
Myget是GNU/Linux下的下载加速器

%prep
%setup -q -n %{name}-%{version}
%patch2 -p1

%build
autoreconf -fisv
./configure  --prefix=%{_prefix}
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
%makeinstall
cd %{buildroot}%{_bindir}
ln -s mytget myget || :

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING INSTALL NEWS README
%{_bindir}/*


%changelog
* Fri Feb 05 2016 Liu Di <liudidi@gmail.com> - 0.1.2-6
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 0.1.2-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.1.2-4
- 为 Magic 3.0 重建

* Sun Jan 07 2007 Liu Di <liudidi@gmail.com> - 0.1.2-1mgc
- update to 0.1.2

* Sat Oct 15 2005 kde <jack@linux.net.cn> - 0.1.1-20050921-1mgc
- initial the spec file for Magic Linux 2.0 
