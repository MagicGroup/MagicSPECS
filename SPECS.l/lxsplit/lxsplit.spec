Name:		lxsplit
Version:	0.2.4
Release:	6%{?dist}
Summary:	File split / merge utility

Group:		Applications/File
License:	GPLv2+
URL:		http://lxsplit.sourceforge.net/
Source:		http://downloads.sourceforge.net/lxsplit/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)	

%description
lxSplit is a simple tool for splitting files and joining the splitted files 
on linux and unix-like platforms. Splitting is done without compression and 
large files (> 4 GB) are supported. lxSplit is fully compatible with the 
HJSplit utility which is available for other operating systems.



%prep
%setup -q

%build
%{__make}  CFLAGS="$RPM_OPT_FLAGS" %{?_smp_flags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__install} -D -m755 lxsplit %{buildroot}/%{_bindir}/lxsplit

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog README COPYING
%{_bindir}/lxsplit

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Oct 03 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.4-1
- new upstream release

* Thu Jul 03 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.3-1
-  Pull new upstream. Drop obsoleted patch and fix defattr

* Sat May 31 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.2-4
- Apply upstream build patch

* Tue May 27 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.2-3
- Fixed cflags, attr and added COPYING

* Sun May 25 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.2-2
- Add dist tag

* Sun May 25 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.2-1
- Upstream spec modified for Fedora

