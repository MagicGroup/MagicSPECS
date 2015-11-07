Name:           cegui06
Version:        0.6.2
Release:        16%{?dist}
Summary:        CEGUI library 0.6 for apps which need this specific version
Group:          System Environment/Libraries
License:        MIT and LGPLv2+
URL:            http://www.cegui.org.uk
# This is
# http://downloads.sourceforge.net/crayzedsgui/CEGUI-0.6.2b.tar.gz
# with the bundled GLEW: RendererModules/OpenGLGUIRenderer/GLEW
# removed as its an older GLEW version which contains
# parts under then non Free SGI OpenGL and GLX licenses
# To regenerate do:
# wget http://downloads.sourceforge.net/crayzedsgui/CEGUI-0.6.2b.tar.gz
# tar xvfz CEGUI-0.6.2b.tar.gz'
# rm -r CEGUI-0.6.2/RendererModules/OpenGLGUIRenderer/GLEW
# tar cvfz CEGUI-0.6.2b-clean.tar.gz
Source0:        CEGUI-0.6.2b-clean.tar.gz
Source1:        http://downloads.sourceforge.net/crayzedsgui/CEGUI-%{version}-DOCS.tar.gz
# Both submitted upstream: http://www.cegui.org.uk/mantis/view.php?id=197
Patch1:         cegui-0.6.0-release-as-so-ver.patch
Patch2:         cegui-0.6.0-userverso.patch
# TODO: submit upstream
Patch3:         cegui-0.6.2-new-DevIL.patch
Patch4:         cegui-0.6.2-new-tinyxml.patch
Patch5:         cegui-0.6.2-gcc46.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  expat-devel
BuildRequires:  freetype-devel > 2.0.0
BuildRequires:  libICE-devel
BuildRequires:  libGLU-devel
BuildRequires:  libSM-devel
BuildRequires:  pcre-devel
BuildRequires:  glew-devel

%description
Crazy Eddie's GUI System is a free library providing windowing and widgets for
graphics APIs / engines. This package contains the older version 0.6 for
apps which cannot be easily ported to 0.7. As such this version has been build
without additional image codecs or xml parsers.


%package devel
Summary:        Development files for cegui06
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libGLU-devel

%description devel
Development files for cegui06


%package devel-doc
Summary:        API documentation for cegui06
Group:          Documentation
Requires:       %{name}-devel = %{version}-%{release}

%description devel-doc
API and Falagard skinning documentation for cegui06


%prep
%setup -qb1 -qn CEGUI-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Permission fixes for debuginfo RPM
chmod -x include/falagard/*.h

# Delete zero length file
rm -f documentation/api_reference/keepme

# Encoding fixes
iconv -f iso8859-1 AUTHORS -t utf8 > AUTHORS.conv && mv -f AUTHORS.conv AUTHORS
iconv -f iso8859-1 TODO -t utf8 > TODO.conv && mv -f TODO.conv TODO
iconv -f iso8859-1 README -t utf8 > README.conv && mv -f README.conv README

# Make makefile happy even though we've removed the (unused) included copy of
# GLEW due to license reasons
mkdir -p RendererModules/OpenGLGUIRenderer/GLEW/GL
touch RendererModules/OpenGLGUIRenderer/GLEW/GL/glew.h
touch RendererModules/OpenGLGUIRenderer/GLEW/GL/glxew.h
touch RendererModules/OpenGLGUIRenderer/GLEW/GL/wglew.h
touch RendererModules/OpenGLGUIRenderer/GLEW/GLEW-LICENSE


%build
%configure --disable-static --disable-samples --disable-lua-module \
    --disable-corona --disable-devil --disable-silly --disable-freeimage \
    --disable-irrlicht-renderer --disable-directfb-renderer \
    --disable-xerces-c --disable-libxml --disable-tinyxml \
    --with-default-xml-parser=ExpatParser \
    --with-default-image-codec=TgaImageCodec \
    --with-pic
# We do not want to get linked against a system copy of ourselves!
sed -i 's|-L%{_libdir}||g' RendererModules/OpenGLGUIRenderer/Makefile
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} 
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Move some things around to make cegui06-devel co-exist peacefully with
# cegui-devel
mkdir -p %{buildroot}/%{_libdir}/CEGUI-0.6
for i in libCEGUIBase libCEGUIExpatParser libCEGUIFalagardWRBase \
         libCEGUIOpenGLRenderer libCEGUITGAImageCodec; do
    rm %{buildroot}/%{_libdir}/$i.so
    ln -s ../$i-%{version}.so %{buildroot}/%{_libdir}/CEGUI-0.6/$i.so
done
mv %{buildroot}/%{_includedir}/CEGUI %{buildroot}/%{_includedir}/CEGUI-0.6
mv %{buildroot}/%{_datadir}/CEGUI %{buildroot}/%{_datadir}/CEGUI-0.6
sed -e 's|/CEGUI|/CEGUI-0.6|g' \
    -e 's|libdir=%{_libdir}|libdir=%{_libdir}/CEGUI-0.6|g' \
    -i %{buildroot}/%{_libdir}/pkgconfig/*.pc
for i in %{buildroot}/%{_libdir}/pkgconfig/*.pc; do
    mv $i `echo $i | sed 's|\.pc\$|-0.6.pc|'`
done


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_libdir}/libCEGUI*-%{version}.so


%files devel
%defattr(-,root,root,-)
%{_libdir}/CEGUI-0.6
%{_libdir}/pkgconfig/CEGUI-OPENGL-0.6.pc
%{_libdir}/pkgconfig/CEGUI-0.6.pc
%{_includedir}/CEGUI-0.6
%{_datadir}/CEGUI-0.6


%files devel-doc
%defattr(-,root,root,-)
%doc documentation/FalagardSkinning.pdf documentation/api_reference


%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.6.2-16
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.6.2-15
- 为 Magic 3.0 重建

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 0.6.2-14
- 为 Magic 3.0 重建

* Sun Apr 28 2013 Liu Di <liudidi@gmail.com> - 0.6.2-12
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.6.2-11
- 为 Magic 3.0 重建

* Fri Nov 02 2012 Liu Di <liudidi@gmail.com> - 0.6.2-10
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 ajax@redhat.com - 0.6.2-8
- Rebuild for new glew soname

* Sun Feb 13 2011 Hans de Goede <hdegoede@redhat.com> - 0.6.2-7
- Fix building with gcc-4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Bruno Wolff III <bruno@wolff.to> - 0.6.2-5
- Rebuild against ogre that uses boost instead of poco.

* Tue Jan 04 2011 Bruno Wolff III <bruno@wolff.to> - 0.6.2-4
- Fix requires to be cegui06-devel rather than cegui-devel

* Mon Jan  3 2011 Hans de Goede <hdegoede@redhat.com> 0.6.2-3
- Update License tag to "MIT and LGPLv2+" and some files did not have
  their copyright header updated when upstream moved from LGPLv2+ to MIT.
  This is fixed in the 0.7.x (and later) versions of cegui.

* Tue Nov  9 2010 Hans de Goede <hdegoede@redhat.com> 0.6.2-2
- Switch to new upstream 0.6.2b tarbal (#650643)

* Sun Nov  7 2010 Hans de Goede <hdegoede@redhat.com> 0.6.2-1
- First release of CEGUI-0.6.2 as cegui06
