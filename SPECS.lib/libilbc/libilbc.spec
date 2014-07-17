# $Revision: 1.7 $, $Date: 2007-02-12 22:09:10 $
#
# Conditional build:
%bcond_with 	static_libs	# don't build static library
#
Summary:	iLBC Speech Coder
Summary(pl.UTF-8):	Koder mowy iLBC
Name:		libilbc
Version:	1.0
Release:	4%{?dist}
License:	Global IP Sound v2.0 (requires registration for non-personal use)
Group:		Libraries
Source0:	http://simon.morlat.free.fr/download/1.3.x/source/ilbc-rfc3951.tar.gz
# Source0-md5:	c53bb4f1d7184789ab90d2d33571e78a
Source1:	http://ilbcfreeware.org/documentation/gips_iLBClicense.pdf
# Source1-md5:	71cee7ed8e5d5440a53845e7043c4cb5
URL:		http://ilbcfreeware.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
iLBC (internet Low Bitrate Codec) is a FREE speech codec suitable for
robust voice communication over IP. The codec is designed for narrow
band speech and results in a payload bit rate of 13.33 kbps with an
encoding frame length of 30 ms and 15.20 kbps with an encoding length
of 20 ms. The iLBC codec enables graceful speech quality degradation
in the case of lost frames, which occurs in connection with lost or
delayed IP packets.

%description -l pl.UTF-8
iLBC (internet Low Bitrate Codec) to darmowy kodek mowy nadajacy się
do komunikacji głosowej po IP. Kodek jest zaprojektowany ograniczonych
łącz, a w efekcie wykorzystuje 13.33 kbit/s przy ramce o długości 30
ms i 15.20 kbit/s przy ramce o długości 20 ms. Kodek iLBC umożliwia
obniżenie jakości mowy w przypadku utraconych ramek, co zdarza się w
przypadku utraty połączenia lub opóźnionych pakietów IP.

%package devel
Summary:	Header files for iLBC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki iLBC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for iLBC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki iLBC.

%package static
Summary:	Static iLBC library
Summary(pl.UTF-8):	Statyczna biblioteka iLBC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static iLBC library.

%description static -l pl.UTF-8
Statyczna biblioteka iLBC.

%prep
%setup -q -n ilbc-rfc3951
cp %{SOURCE1} .

%build
autoreconf -fisv
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS *.pdf
%attr(755,root,root) %{_libdir}/libilbc.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libilbc.so
%{_libdir}/libilbc.la
%{_includedir}/ilbc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libilbc.a
%endif

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建
