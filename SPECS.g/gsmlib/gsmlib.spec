Summary: 	Library and utilities to access GSM mobile phones
Name: 	 	gsmlib
Version: 	1.11
Release: 	0.2%{?dist}
License:	GPL
Group:		Communications
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

%package  	devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C

%description devel
Libraries and includes files for developing programs based on %name.

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
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.11-0.2
- 为 Magic 3.0 重建


