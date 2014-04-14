Summary: 	Library and utilities to access GSM mobile phones
Summary(zh_CN.UTF-8): 访问 GSM 手机的库和工具
Name: 	 	gsmlib
Version: 	1.11
Release: 	0.3%{?dist}
License:	GPL
Group:		Application/Communications
Group(zh_CN.UTF-8): 应用程序/通信
URL:		http://www.pxh.de/fs/gsmlib/index.html
Source0:	%{name}-pre1.11-041028.tar.bz2
Patch0:		gsmlib-1.11-gcc41.patch
Patch1:		gsmlib-1.11-gcc43.patch
Patch2:		gsmlib-1.11-include-gcc34-fix.patch
Patch3:		gsmlib-1.11-linkfix.diff
BuildRequires:	gettext
BuildRequires:	bison
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This distribution contains a library to access GSM mobile phones through GSM
modems. Features include:
    * modification of phonebooks stored in the mobile phone or on the SIM card
    * reading and writing of SMS messages stored in the mobile phone
    * sending and reception of SMS messages 

Additionally, some simple command line programs are provided to use these
functionalities. 

%description -l zh_CN.UTF-8 
访问 GSM 手机的库和工具，功能包括：修改存储在手机或 SIM 卡上的电话本、读取和
写入存储在手机上的短信、发送和接收短信。

%package  	devel
Summary: 	Header files and static libraries from %name
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: 		Development/C
Group(zh_CN.UTF-8): 开发/库

%description devel
Libraries and includes files for developing programs based on %name.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep

%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export LIBS="-lstdc++"

%configure

make %{?_smp_mflags}
										
%install
rm -rf %{buildroot}

%makeinstall
magic_rpm_clean.sh
%find_lang %name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README ABOUT-NLS COPYING ChangeLog NEWS TODO
%{_bindir}/gsm*
%{_mandir}/man1/gsm*
%{_mandir}/man7/gsm*
%{_mandir}/man8/gsm*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%name/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la


%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 1.11-0.3
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.11-0.2
- 为 Magic 3.0 重建


