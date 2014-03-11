%global actualname cantarell

%global fontname abattis-%{actualname}
%global fontconf 31-cantarell.conf

%global archivename1 Cantarell-Bold
%global archivename2 Cantarell-Regular

Name: %{fontname}-fonts
Version: 0.0.12
Release: 1%{?dist}
Summary: Cantarell, a Humanist sans-serif font family
Summary(zh_CN.UTF-8): Cantarell，一个人性化的无衬线字体集

Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
License: OFL
URL: http://abattis.org/cantarell/
Source0: http://download.gnome.org/sources/%{actualname}-fonts/0.0/%{actualname}-fonts-%{version}.tar.xz

BuildArch: noarch
BuildRequires: fontpackages-devel
BuildRequires: fontforge
Requires: fontpackages-filesystem

%description
Cantarell is a set of fonts designed by Dave Crossland.
It is a sans-serif humanist typeface family.

%description -l zh_CN.UTF-8
Cantarell 是由 Dave Crossland 设计的一套字体。
这是一个人性化的无衬线字体集。

%prep
%setup -q -n %{actualname}-fonts-%{version}

%build
%configure
make %{?_smp_mflags}
ls -l ./src/
fontforge -lang=ff -c 'Open($1); Generate($2);' src/%{archivename1}.sfd %{archivename1}.otf
fontforge -lang=ff -c 'Open($1); Generate($2);' src/%{archivename2}.sfd %{archivename2}.otf

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.otf %{buildroot}%{_fontdir}
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -m 0644 -p fontconfig/%{fontconf} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}
#不需要
#magic_rpm_clean.sh
%_font_pkg -f %{fontconf} *.otf
%doc COPYING NEWS README

%changelog
* Tue May 14 2013 Liu Di <liudidi@gmail.com> - 0.0.12-1
- 重新编译


