%global	gem_name	opengl

%global	bootstrap	0

# examples/OrangeBook/: BSD
# examples/NeHe: KILLED (license unclear)
# examples/RedBook/ SGI = MIT
# examples/misc/OGLBench.rb: GPL+ or Artistic
# examples/misc/fbo_test.rb ??? KILLED
# examples/misc/trislam.rb: GPL+ or Artistic

Name:		rubygem-%{gem_name}
Version:	0.9.2
Release:	7%{?dist}

Summary:	An OpenGL wrapper for Ruby
Group:	Development/Languages
License:	MIT
URL:		https://github.com/drbrain/opengl
# Source0:	https://rubygems.org/gems/%%{gem_name}-%%{version}.gem
# The above gem file contains files with unclear license,
# we use a regenerated gem as a Source0 with such files
# removed.
# Source0 is generated using Source1.  
Source0:	%{gem_name}-%{version}-clean.gem
Source1:	create-clean-opengl-gem.sh
# http://www.gnu.org/licenses/old-licenses/gpl-1.0.txt
Source2:	GPLv1.rubygem_opengl

# MRI (CRuby) only
BuildRequires:	ruby-devel
BuildRequires:	rubygems-devel
BuildRequires:	libGL-devel
BuildRequires:	libGLU-devel
BuildRequires:	freeglut-devel
# %%check
%if 0%{?bootstrap} < 1
BuildRequires:	rubygem(minitest) >= 5
BuildRequires:	%{_bindir}/xvfb-run
BuildRequires:	mesa-dri-drivers
BuildRequires:	rubygem(glu)
BuildRequires:	rubygem(glut)
%endif
%if 0%{?fedora} <= 21
# Install this for compatibility
Requires:	rubygem(glu)
Requires:	rubygem(glut)
%endif


%description
An OpenGL wrapper for Ruby. ruby-opengl contains bindings for OpenGL and the
GLU and GLUT libraries.


%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
License:	MIT and BSD and (GPL+ or Artistic)
BuildArch:	noarch

%description	doc
Documentation for %{name}

%prep
%setup -q -c -T

# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}-clean
gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec

find examples/ -type f -print0 | xargs --null file | \
	grep CRLF | sed -e 's|:.*$||' | \
	while read f
do
	sed -i -e 's|\r||' $f
done

%if 0%{?fedora} >= 21
sed -i.minitest \
	-e 's|MiniTest::Unit::TestCase|Minitest::Test|' \
	lib/opengl/test_case.rb
%endif

gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}/
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

install -cpm 644 %{SOURCE2} \
	%{buildroot}%{gem_instdir}/examples/misc/

%if 0%{?fedora} >= 21
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd

%else
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
mv %{buildroot}%{gem_instdir}/lib/%{gem_name}/ \
	%{buildroot}%{gem_extdir_mri}/lib/

%endif

# cleanups
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.autotest .gemtest .gitignore .travis.yml \
	Manifest.txt \
	Rakefile* \
	docs/build_install.txt \
	ext/ \
	test/

find examples/ utils/ -type f -perm /100 \
	-exec chmod ugo-x {} \;

popd

rm -f %{buildroot}%{gem_extdir_mri}/lib/opengl/test_case.rb

%check
%if 0%{?bootstrap} < 1
pushd .%{gem_instdir}

%if 0%{?fedora} >= 21
cat > test/unit.rb << EOF
gem "minitest"
require "minitest/autorun"
EOF
%endif

xvfb-run \
	-s "-screen 0 640x480x24" \
	ruby \
%if 0%{?fedora} >= 21
		-Ilib:.:./ext \
%else
		-Ilib:.:./ext/opengl \
%endif
		-e "Dir.glob('test/test_*.rb').each { |f| require f }" \
		|| echo "please check this later"
popd
%endif

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/MIT-LICENSE
%doc	%{gem_instdir}/History.rdoc
%doc	%{gem_instdir}/README.rdoc

%{gem_libdir}/
%{gem_extdir_mri}/

%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/examples/
%doc	%{gem_instdir}/utils/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.9.2-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.2-5
- Enable test again

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.2-4
- F-22: Rebuild for ruby 2.2
- Bootstrap, once disable test

* Sun Jan 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.2-3
- Enable test

* Sun Jan 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.2-1
- 0.9.2
- bootstrap, once disabling test

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-4
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Wed Oct 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-2
- Misc fixes with review (bug 1024168)

* Tue Oct 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-1
- Initial package
