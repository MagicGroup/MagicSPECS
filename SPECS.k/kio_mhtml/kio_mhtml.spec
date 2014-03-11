Name: kio_mhtml
Summary: kio_mhtml is a KDE I/O Slave for mht and eml files.
Summary(zh_CN.UTF-8): kio_mhtml是一个查看mht和eml文件的KDE I/O Slave
Version: 0.3.4
Release: 4%{?dist}
License: GPL
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Source: %{name}-%{version}.tgz
Patch:	kio_mhtml-0.3.4-admin.patch
BuildRoot: %{_tmppath}/build-root-%{name}
Packager: KanKer
Url: http://www.kde-apps.org/content/show.php?content=14315

%description
kio_mhtml v0.3.4, uses KMail's fonts and colors in the HTML files coming from
text-only EML files. This way kio_mhtml v0.3.4 wil have the same
'look and feel' as KMail.

%description -l zh_CN.UTF-8
kio_mhtml v0.3.4，一个查看mht和eml文件的KDE I/O Slave

%prep

%setup -q
%patch -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lDCOP \-lkio/g' protocol/Makefile
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT/usr/share/doc/HTML/{ar,br,bs,ca,cs,cy,da,de,el,en_GB,es,et,fi,fr,ga,he,hi,hu,is,it,lt,mt,nb,nl,pa,pl,pt*,ro,ru,rw,sk,sr*,sv,ta,tr,xx}
rm -rf $RPM_BUILD_ROOT/usr/share/locale/{ar,br,bs,ca,cs,cy,da,de,el,en_GB,es,et,fi,fr,ga,he,hi,hu,is,it,lt,mt,nb,nl,pa,pl,pt*,ro,ru,rw,sk,sr*,sv,ta,tr,xx}

%clean
rm -rf $RPM_BUILD_ROOT

%files 

%defattr(-,root,root,0755)
/usr
%exclude /usr/*/debug*

