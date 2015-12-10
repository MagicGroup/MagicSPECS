Name:           leafpad
Version:        0.8.18.1
Release:        4%{?dist}

Summary:        GTK+ based simple text editor
Summary(zh_CN.UTF-8): 基于 GTK 的简单文本编辑器

Group:          Applications/Editors
Group(zh_CN.UTF-8):	应用程序/编辑器
License:        GPLv2+
URL:            http://tarot.freeshell.org/leafpad/
Source0:        http://savannah.nongnu.org/download/leafpad/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.4 desktop-file-utils
BuildRequires:	gettext
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Leafpad is a GTK+ based simple text editor. The user interface is similar to
Notepad. It aims to be lighter than GEdit and KWrite, and to be as useful as
them.

%description -l zh_CN.UTF-8
Leafpad 是一个基于 GTK 的简单文本编辑器。用户界面类似记事本。

%prep
%setup -q

%build
%configure --enable-chooser
make %{?_smp_mflags}
cat>>data/leafpad.desktop<<EOF
StartupNotify=true
GenericName=Text Editor
EOF

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install --vendor=magic \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  --add-category GTK \
  --delete-original \
  $RPM_BUILD_ROOT%{_datadir}/applications/leafpad.desktop
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/leafpad.*

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 0.8.18.1-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.8.18.1-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.8.18.1-2
- 为 Magic 3.0 重建


