%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define pyver %(%{__python} -c "import sys ; print sys.version[:3]")
%define py_incdir %{_includedir}/python%{pyver}

Summary:       Python's own image processing library
Name:          python-imaging
Version:       1.1.7
Release:       5%{?dist}

License:       MIT
Group:         System Environment/Libraries

Source0:       http://effbot.org/downloads/Imaging-%{version}.tar.gz
Patch1:        %{name}-lib64.patch
Patch2:        %{name}-giftrans.patch
Patch3:        %{name}-1.1.6-sane-types.patch
Patch4:        %{name}-shebang.patch
Patch5:        python-imaging-fix-freetype2.patch
URL:           http://www.pythonware.com/products/pil/
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel, libjpeg-devel, zlib-devel, freetype-devel
BuildRequires: tkinter, tk-devel, lcms-devel
%ifnarch s390 s390x
BuildRequires: sane-backends-devel
%endif

%description
Python Imaging Library

The Python Imaging Library (PIL) adds image processing capabilities
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

Notice that in order to reduce the package dependencies there are
three subpackages: devel (for development); tk (to interact with the
tk interface) and sane (scanning devices interface).

%package devel
Summary: Development files for python-imaging
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, python-devel
Requires: libjpeg-devel
Requires: zlib-devel

%description devel
Development files for python-imaging.

%ifnarch s390 s390x
%package sane
Summary: Python Module for using scanners
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description sane
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.
%endif

%package tk
Summary: Tk interface for python-imaging
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: tkinter
Obsoletes: %{name} < 1.1.6-3
Conflicts: %{name} < 1.1.6-3

%description tk
This package contains a Tk interface for python-imaging.

%prep
%setup -q -n Imaging-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .sane-types
%patch4 -p1 -b .shebang
%patch5 -p1 -b .freetype2

# fix the interpreter path for Scripts/*.py
cd Scripts
for scr in *.py
do
  sed -e "s|/usr/local/bin/python|%{_bindir}/python|"  $scr > tmp.py
  mv tmp.py $scr
  chmod 755 $scr
done

%build
# Is this still relevant? (It was used in 1.1.4)
#%ifarch x86_64
#   CFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" \
#%endif

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%ifnarch s390 s390x
pushd Sane
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{py_incdir}/Imaging
install -m 644 libImaging/*.h $RPM_BUILD_ROOT/%{py_incdir}/Imaging
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%ifnarch s390 s390x
pushd Sane
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

# There is no need to ship the binaries since they are already packaged
# in %doc
rm -rf $RPM_BUILD_ROOT%{_bindir}

# Separate files that need Tk and files that don't
echo '%%defattr (0644,root,root,755)' > files.main
echo '%%defattr (0644,root,root,755)' > files.tk
p="$PWD"

pushd $RPM_BUILD_ROOT%{python_sitearch}/PIL
for file in *; do
    case "$file" in
    ImageTk*|SpiderImagePlugin*|_imagingtk.so)
        what=files.tk
        ;;
    *)
        what=files.main
        ;;
    esac
    echo %{python_sitearch}/PIL/$file >> "$p/$what"
done
popd


%check
# need some hacks
sed -i "s|ROOT = \".\"|ROOT = \"$RPM_BUILD_ROOT%{python_sitearch}\"|" selftest.py
ln -s $PWD/Images $RPM_BUILD_ROOT%{python_sitearch}/Images
%{__python} selftest.py
rm $RPM_BUILD_ROOT%{python_sitearch}/Images

%clean
rm -rf $RPM_BUILD_ROOT


%files -f files.main
%defattr (-,root,root,-)
%doc README CHANGES
%{python_sitearch}/PIL.pth
%dir %{python_sitearch}/PIL

%files devel
%defattr (0644,root,root,755)
%{py_incdir}/Imaging
%doc Docs Scripts Images

%ifnarch s390 s390x
%files sane
%defattr (0644,root,root,755)
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%if 0%{?fedora} >= 9
%{python_sitearch}/pysane*egg-info
%endif
%{python_sitearch}/_sane.so
%{python_sitearch}/sane.py*
%endif

%files tk -f files.tk

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.7-5
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Liu Di <liudidi@gmail.com> - 1.1.7-4
- 为 Magic 3.0 重建

