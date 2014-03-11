Name:           qt-creator
Version:        2.6.1
Release:        1%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt
Summary(zh_CN):	Qt 的跨平台轻量级 IDE

Group:          Development/Tools
Group(zh_CN):	开发/工具
License:        LGPLv2 with exceptions
URL:            http://www.qtsoftware.com/developer/qt-creator
Source0:        http://download.qtsoftware.com/qtcreator/%name-%version-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:       qtcreator.desktop
Source2:       qtcreator-bin-wrapper

Requires:       hicolor-icon-theme

#required for demos/examples
Requires:       qt4-demos
Requires:       qt4-examples

BuildRequires:  qt4-devel >= 4.6.0
BuildRequires:  desktop-file-utils

%description
Qt Creator (previously known as Project Greenhouse) is a new,
lightweight, cross-platform integrated  development environment (IDE)
designed to make development with the Qt application framework
even faster and easier.

%description -l zh_CN
QT 的跨平台轻量级 IDE。

%prep
%setup -q -n %{name}-%{version}-src

%build
QTDIR="%{_qt4_prefix}" ; export QTDIR ; \
PATH="%{_qt4_bindir}:$PATH" ; export PATH ; \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \

qmake-qt4 -r IDE_LIBRARY_BASENAME=%{_lib}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT/%{_prefix}

for i in 16 24 32 48 64 128 256
do
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/${i}x${i}/apps
# link it to %{_datadir}/pixmaps/qtcreator_logo_${i}.png
ln -s ../../../../pixmaps/qtcreator_logo_${i}.png \
 $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/${i}x${i}/apps/Nokia-QtCreator.png

done

desktop-file-install                                    \
--add-category="Development"                            \
--dir=%{buildroot}%{_datadir}/applications              \
%{SOURCE1}

install -Dp -m 755 %{SOURCE2} $RPM_BUILD_ROOT/%{_bindir}/qtcreator

%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :



%files
%defattr(-,root,root,-)
%doc README LICENSE.LGPL LGPL_EXCEPTION.TXT
%{_bindir}/qtcreator
%{_bindir}/qtpromaker
%{_bindir}/qtcreator_process_stub
%{_bindir}/sdktool
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/icons/hicolor/*/apps/*.png

%changelog

