%define filippov_version 1.0.7pre44
%define fontdir %{_datadir}/fonts/default/Type1
%define catalogue /etc/X11/fontpath.d

Summary: Free versions of the 35 standard PostScript fonts.
Summary(zh_CN.UTF-8): 35 种 PostScript 字体的免费版本
Name: urw-fonts
Version: 2.4
Release: 9%{?dist}
Source: ftp://ftp.gnome.ru/fonts/urw/release/urw-fonts-%{filippov_version}.tar.bz2
URL: ftp://ftp.gnome.ru/fonts/urw/release/
# URW holds copyright
# No version specified
License: GPL+
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch

Requires(post): fontconfig
Requires(postun): fontconfig

%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.

Install the urw-fonts package if you need free versions of standard
PostScript fonts.

%description -l zh_CN.UTF-8
该软件包包括 35 种免费的、高质量的、PostScript(TM) 字体。
它们由 URW++ Design 和 Development GmbH 在 GPL 的条款下贡献。
fonts.dir 文件字体名与字体的原始 Adobe 名想匹配 (Times, Helvetica, 等.)。

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{fontdir}
install -m 0644 *.afm *.pfb $RPM_BUILD_ROOT%{fontdir}/

# Touch ghosted files
touch $RPM_BUILD_ROOT%{fontdir}/{fonts.{dir,scale,cache-1},encodings.dir}

# Install catalogue symlink
mkdir -p $RPM_BUILD_ROOT%{catalogue}
ln -sf %{fontdir} $RPM_BUILD_ROOT%{catalogue}/fonts-default
magic_rpm_clean.sh

%post
{
   umask 133
   mkfontscale %{fontdir} || :
   `which mkfontdir` %{fontdir} || :
   fc-cache %{_datadir}/fonts
} &> /dev/null || :

%postun
{
   if [ "$1" = "0" ]; then
      fc-cache %{_datadir}/fonts
   fi
} &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc COPYING README README.tweaks
%dir %{_datadir}/fonts/default
%dir %{fontdir}
%{catalogue}/fonts-default
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.scale
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{fontdir}/encodings.dir
%{fontdir}/*.afm
%{fontdir}/*.pfb

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.4-9
- 为 Magic 3.0 重建

* Tue Feb 21 2012 Liu Di <liudidi@gmail.com> - 2.4-8
- 为 Magic 3.0 重建


