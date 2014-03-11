%global codate 20121009

Name:           gl-manpages
Version:        1.1
Release:        3.%{codate}%{?dist}
Summary:        OpenGL manpages

License:        MIT and Open Publication
URL:            http://www.opengl.org/wiki/Getting_started/XML_Toolchain_and_Man_Pages
# see Source1
Source0:        gl-manpages-%{version}-%{codate}.tar.xz
Source1:        make-gl-man-snapshot.sh
# FIXME: Bundle mathml and the Oasis dbmathl until they are packaged
Source2:        http://www.oasis-open.org/docbook/xml/mathml/1.1CR1/dbmathml.dtd
Source3:        http://www.w3.org/Math/DTD/mathml2.tgz
# FIXME  These are the old gl-manpages source which 
# still have some manpages that khronos doesn't. 
# Ship until somebody in the know helps figuring whats what.
# When matching install the kronos version.
Source4:        gl-manpages-1.0.1.tar.bz2

BuildArch:      noarch

BuildRequires:  libxslt docbook-style-xsl

%description
OpenGL manpages

%prep
%setup -q -n %{name}-%{version}-%{codate}
tar xzf %{SOURCE3}
cp -av %{SOURCE2} mathml2/
tar xjf %{SOURCE4}


%build
# FIXME Figure out how to build the GLSL manpages
# FIXME Figure out how to silence the author/version etc warnings
for MAN in man4 man3 man ; do
	pushd $MAN
	ls -1 *.xml | xargs -n1 xsltproc --noout --nonet --path ../mathml2/ /usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl
	popd
done


%install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
cp -n {man4,man3,man}/*.3G $RPM_BUILD_ROOT%{_mandir}/man3/
# install the old manpages source with 3gl -> 3G
# when matchin don't clobber the khronos version
for MANP in `find gl-manpages-1.0.1 -name *.3gl` ; do
	FN=${MANP//*\//}
	cp -a -n $MANP $RPM_BUILD_ROOT%{_mandir}/man3/${FN/.3gl/.3G}
	find $RPM_BUILD_ROOT%{_mandir}/man3/ -type f -size -100b | xargs sed -i -e 's/\.3gl/\.3G/'
done


%files
%{_mandir}/man3/*


%changelog
* Mon Oct 15 2012 Yanko Kaneti <yaneti@declera.com> - 1.1-3.%{codate}
- Fix symlinked man variants. 
- Preserve timestamps on the older gl-manpages.

* Tue Oct  9 2012 Yanko Kaneti <yaneti@declera.com> - 1.1-2.%{codate}
- Re-add the older gl-manpages for those not present in khronos

* Tue Oct  9 2012 Yanko Kaneti <yaneti@declera.com> - 1.1-1.%{codate}
- Try building from source

* Wed Sep  5 2012 Yanko Kaneti <yaneti@declera.com> - 1.0.1-1
- Initial split from mesa
