Name:           magic-bookmarks
Version:        3
Release:        6%{?dist}
Summary:        Magic bookmarks
Summary(zh_CN.UTF-8):	Magic 的默认书签
Group:          Applications/Internet
Group(zh_CN.UTF-8):	应用程序/互联网
License:        GFDL
URL:            http://www.magiclinux.org/
Source0:        default-bookmarks.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Provides:       system-bookmarks


%description
This package contains the default bookmarks for Magic.

%description -l zh_CN.UTF-8
这个包包含了 Magic 的 Firefox 3 的默认书签。

%prep
# We are nihilists, Lebowski.  We believe in nassing.

%build
# We are nihilists, Lebowski.  We believe in nassing.

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/bookmarks
install -p -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/bookmarks


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_datadir}/bookmarks
%{_datadir}/bookmarks/default-bookmarks.html

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3-6
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 3-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3-4
- 为 Magic 3.0 重建

* Sun Jan 15 2012 Liu Di <liudidi@gmail.com> - 3-3
- 为 Magic 3.0 重建

* Sat Jun 07 2008 Liu Di <liudidi@gmail.com> - 3-1mgc
- 首次打包
