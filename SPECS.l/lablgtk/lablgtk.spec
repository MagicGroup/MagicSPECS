Name:           lablgtk
Version:        2.14.2
Release:        1%{?dist}

Summary:        Objective Caml interface to gtk+
Summary(zh_CN.UTF-8): Objective Caml 的 gtk+ 接口

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        LGPLv2 with exceptions

URL:            http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgtk.html
Source:         http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgtk-%{version}.tar.gz

Patch0:         ocaml-lablgtk-2.12.0-gnome-ui-init-header.patch
Patch1:         ocaml-lablgtk-2.12.0-ocaml-4-fix.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       ocaml-lablgtk = %{version}

BuildRequires:	ncurses-devel
BuildRequires:  gnome-panel-devel
BuildRequires:  gtk2-devel
#BuildRequires:  gtkglarea2-devel
BuildRequires:  gtkspell-devel
BuildRequires:  libXmu-devel
BuildRequires:  libglade2-devel
BuildRequires:  libgnomecanvas-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  librsvg2-devel
BuildRequires:  ocaml >= 3.10.1
BuildRequires:  ocaml-camlp4-devel
#BuildRequires:  ocaml-lablgl-devel >= 1.03
BuildRequires:  ocaml-ocamldoc
BuildRequires:  zlib-devel
#BuildRequires:  gtksourceview-devel


%define _use_internal_dependency_generator 0
%define __find_requires /usr/lib/rpm/ocaml-find-requires.sh -i GtkSourceView_types
%define __find_provides /usr/lib/rpm/ocaml-find-provides.sh


%description
LablGTK is is an Objective Caml interface to gtk+.

It uses the rich type system of Objective Caml 3 to provide a strongly
typed, yet very comfortable, object-oriented interface to gtk+. This
is not that easy if you know the dynamic typing approach taken by
gtk+.

%description -l zh_CN.UTF-8
LablGTK 是一个 Objective Caml 的 gtk+ 接口。

它使用 Objective Caml 3 的 rich 类型系统以提供一种强大的类面向 gtk+ 接口。

%package doc
Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
Summary:        Documentation for LablGTK
Summary(zh_CN.UTF-8): %name 的文档
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%description doc -l zh_CN.UTF-8
%name 的文档

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q -n lablgtk-%{version}

#%patch0 -p1
%patch1 -p1

# version information in META file is wrong
perl -pi -e 's|version="1.3.1"|version="%{version}"|' META


%build
%configure 
perl -pi -e "s|-O|$RPM_OPT_FLAGS|" src/Makefile
make world
make doc CAMLP4O="camlp4o -I %{_libdir}/ocaml/camlp4/Camlp4Parsers"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make install \
     BINDIR=$RPM_BUILD_ROOT%{_bindir} \
     LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
     INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2 \
     DLLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
cp META $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2

# Remove unnecessary *.ml files (ones which have a *.mli).
pushd $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2
for f in *.ml; do \
  b=`basename $f .ml`; \
  if [ -f "$b.mli" ]; then \
    rm $f; \
  fi; \
done
popd

# Remove .cvsignore files from examples directory.
find examples -name .cvsignore -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING CHANGES
%dir %{_libdir}/ocaml/lablgtk2
%{_libdir}/ocaml/lablgtk2/*.cmi
%{_libdir}/ocaml/lablgtk2/*.cmxs
%{_libdir}/ocaml/lablgtk2/*.cma
%{_libdir}/ocaml/stublibs/*.so
%{_bindir}/gdk_pixbuf_mlsource
%{_bindir}/lablgladecc2
%{_bindir}/lablgtk2


%files devel
%defattr(-,root,root,-)
%doc README COPYING CHANGES
%dir %{_libdir}/ocaml/lablgtk2
%{_libdir}/ocaml/lablgtk2/META
%{_libdir}/ocaml/lablgtk2/*.a
%{_libdir}/ocaml/lablgtk2/*.cmxa
%{_libdir}/ocaml/lablgtk2/*.cmx
%{_libdir}/ocaml/lablgtk2/*.mli
%{_libdir}/ocaml/lablgtk2/*.ml
%{_libdir}/ocaml/lablgtk2/*.h
%{_libdir}/ocaml/lablgtk2/gtkInit.cmo
%{_libdir}/ocaml/lablgtk2/gtkInit.o
%{_libdir}/ocaml/lablgtk2/gtkThInit.cmo
%{_libdir}/ocaml/lablgtk2/gtkThread.cmo
%{_libdir}/ocaml/lablgtk2/gtkThread.o
%{_libdir}/ocaml/lablgtk2/propcc
%{_libdir}/ocaml/lablgtk2/varcc


%files doc
%defattr(-,root,root,-)
%doc examples doc/html


%changelog

