%global svndate 20120626
%global svnrev  249

Name:		jsoncpp	
Version:	0.6.0
Release:	0.2.%{svndate}svn%{svnrev}%{?dist}
Summary:	API for manipulating JSON
License:	MIT or Public Domain
URL:		http://jsoncpp.sourceforge.net/
# Need to use svn.
# svn export https://jsoncpp.svn.sourceforge.net/svnroot/jsoncpp/trunk/jsoncpp jsoncpp
# tar cfj jsoncpp-20120626svn249.tar.bz2 jsoncpp
Source0:	%{name}-%{svndate}svn%{svnrev}.tar.bz2
Source1:	jsoncpp.pc
Patch0:		jsoncpp-optflags.patch
BuildRequires:	scons

%description
JSONCPP provides a simple API to manipulate JSON values, and handle 
serialization and unserialization to strings.

%package devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Headers	and libraries for JSONCPP

%description devel
Headers and libraries for JSONCPP.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .optflags
sed -i 's|@@OPTFLAGS@@|%{optflags}|g' SConstruct

%build
scons platform=linux-gcc

# Now, lets make a proper shared lib. :P
g++ -o libjsoncpp.so.0.0.0 -shared -Wl,-soname,libjsoncpp.so.0 buildscons/linux-gcc-*/src/lib_json/*.os -lpthread

%install
mkdir -p %{buildroot}%{_libdir}
cp -a libjsoncpp.so.0.0.0 %{buildroot}%{_libdir}/
pushd %{buildroot}%{_libdir}
ln -s libjsoncpp.so.0.0.0 libjsoncpp.so.0
ln -s libjsoncpp.so.0.0.0 libjsoncpp.so
popd
mkdir -p %{buildroot}%{_includedir}/jsoncpp/
cp -a include/json %{buildroot}%{_includedir}/jsoncpp/
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
cp -a %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
sed -i 's|@@LIBDIR@@|%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/jsoncpp.pc

%check
scons platform=linux-gcc check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS.txt README.txt version doc/
%{_libdir}/libjsoncpp.so.*

%files devel
%{_includedir}/jsoncpp/
%{_libdir}/libjsoncpp.so
%{_libdir}/pkgconfig/jsoncpp.pc

%changelog
* Thu Jan 10 2013 Liu Di <liudidi@gmail.com> - 0.6.0-0.2.20120626svn249
- 为 Magic 3.0 重建

* Tue Jun 26 2012 Tom Callaway <spot@fedoraproject.org> 0.6.0-0.1.20120626svn249
- initial package
