Name:		oniguruma
Version:	5.9.6
Release:	2%{?dist}
Summary:	Regular expressions library
Summary(zh_CN.UTF-8): 正则表达式库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	BSD
URL:		http://www.geocities.jp/kosako3/oniguruma/
Source0:	http://www.geocities.jp/kosako3/oniguruma/archive/onig-%{version}.tar.gz
# FIXME
# Don't know exactly why, however without Patch0 onig_new returns
# NULL reg variable
Patch0:		oniguruma-5.9.2-onig_new-returns-NULL-reg.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	ruby >= 1.8
#Requires:	

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)

%description -l zh_CN.UTF-8
这是一个正则表达式库，可以支持多种编码，包括 UTF-8, GB18030 等。
支持的 API 包括 GNU, POSIX 和本地支持。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n onig-%{version}
%patch0 -p1 -b .nullreg
%{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in

for f in \
	README.ja \
	doc/API.ja \
	doc/FAQ.ja \
	doc/RE.ja
	do
	iconv -f EUC-JP -t UTF-8 $f > $f.tmp && \
		( touch -r $f $f.tmp ; %{__mv} -f $f.tmp $f ) || \
		%{__rm} -f $f.tmp
done

%build
%configure \
	--disable-static \
	--with-rubydir=%{_bindir}
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -c -p"
find $RPM_BUILD_ROOT -name '*.la' \
	-exec %{__rm} -f {} ';'
magic_rpm_clean.sh

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%check
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc	AUTHORS
%doc	COPYING
%doc	HISTORY
%doc	README
%doc	index.html
%lang(ja)	%doc	README.ja
%lang(ja)	%doc	index_ja.html

%{_libdir}/libonig.so.*

%files devel
%defattr(-,root,root,-)
%doc	doc/API
%doc	doc/FAQ
%doc	doc/RE
%lang(ja)	%doc	doc/API.ja
%lang(ja)	%doc	doc/FAQ.ja
%lang(ja)	%doc	doc/RE.ja

%{_bindir}/onig-config
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libonig.so
%{_includedir}/onig*.h

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 5.9.6-2
- 为 Magic 3.0 重建

* Wed Mar 25 2015 Liu Di <liudidi@gmail.com> - 5.9.6-1
- 更新到 5.9.6

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 5.9.2-4
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 5.9.2-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.2-1
- 5.9.2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-2
- F-11: Mass rebuild

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Thu Dec 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-1
- 5.9.1

* Wed Dec  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.0-1
- Initial packaging

