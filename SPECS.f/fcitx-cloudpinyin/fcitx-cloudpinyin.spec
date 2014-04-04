Name:		fcitx-cloudpinyin
Version:	0.3.3
Release:	1%{?dist}
Summary:	Cloudpinyin module for fcitx
Summary(zh_CN.UTF-8): fcitx 的云拼音模块
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv2+
URL:		https://fcitx-im.org/wiki/Cloudpinyin
Source0:	http://download.fcitx-im.org/fcitx-cloudpinyin/%{name}-%{version}.tar.xz

BuildRequires:	cmake, fcitx-devel, gettext, intltool, libcurl-devel, pkgconfig
Requires:	fcitx, fcitx-pinyin

%description
Cloudpinyin is Fcitx addon that will add one candidate word to your pinyin
list. It current support four provider, Sogou, QQ, Baidu, Google.

%description -l zh_CN.UTF-8
这是一个 fcitx 的模块，它可以给你的输入法的候选词增加选择，现在支持四种云端，
搜狗、QQ、百度和谷歌。

%prep
%setup -q -n %{name}-%{version}


%build
mkdir -pv build
pushd build
%cmake ..
make %{?_smp_mflags} VERBOSE=1
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
popd
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING 
%{_datadir}/fcitx/configdesc/*.desc
%{_datadir}/fcitx/addon/*.conf
%{_libdir}/fcitx/*.so


%changelog
* Wed Apr 02 2014 Liu Di <liudidi@gmail.com> - 0.3.3-1
- 更新到 0.3.3

* Fri Aug 23 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2
- Remove fcitx-0.3.0-logging.patch
- Requires fcitx-pinyin
- Update URL and Source0 URL
- Revise description following upstream wiki

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> - 0.3.0-3
- fix FTBFS with fcitx >= 4.2.7

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Liang Suilong <liangsuilong@gmail.com> - 0.3.0-1
- Upstream to fcitx-cloudpinyin-0.3.0

* Sun Jul 29 2012  Liang Suilong <liangsuilong@gmail.com> - 0.2.3-1
- Upstream to fcitx-cloudpinyin-0.2.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012  Liang Suilong <liangsuilong@gmail.com> - 0.2.1-1
- Upstream to fcitx-cloudpinyin-0.2.1

* Sun Feb 26 2012 Liang Suilong <liangsuilong@gmail.com> - 0.2.0-1
- Initial Package
