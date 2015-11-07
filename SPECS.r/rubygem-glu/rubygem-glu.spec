%global	gem_name	glu

%global	need_bootstrap	0

Name:		rubygem-%{gem_name}
Version:	8.2.1
Release:	8%{?dist}

Summary:	Glu bindings for the opengl gem
License:	MIT
URL:		https://github.com/larskanis/glu
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	rubygems-devel 
BuildRequires:	ruby-devel
BuildRequires:	libGL-devel
BuildRequires:	libGLU-devel
# %%check
%if 0%{?need_bootstrap} < 1
BuildRequires:	rubygem(minitest) >= 5
BuildRequires:	rubygem(opengl)
BuildRequires:	%{_bindir}/xvfb-run
BuildRequires:	mesa-dri-drivers
BuildRequires:	rubygem(opengl) >= 0.9
BuildRequires:	rubygem(glut)
%endif

%description
Glu bindings for the opengl gem.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd


pushd %{buildroot}%{gem_instdir}
rm -rf \
	.autotest .gemtest .gitignore .travis.yml \
	Rakefile \
	ext/ \
	test/
popd

%check
%if 0%{?need_bootstrap} < 1
pushd .%{gem_instdir}

%ifarch %arm
exit 0
%endif

xvfb-run \
	-s "-screen 0 640x480x24" \
	ruby \
		-Ilib:.:./ext \
		-e "Dir.glob('test/test_*.rb').each { |f| require f }"
popd
%endif

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/MIT-LICENSE
%doc	%{gem_instdir}/History.rdoc
%doc	%{gem_instdir}/Manifest.txt
%doc	%{gem_instdir}/README.rdoc

%{gem_libdir}/
%{gem_extdir_mri}/

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 8.2.1-8
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 8.2.1-7
- 为 Magic 3.0 重建

* Tue Jul  7 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.2.1-6
- Disable test on arm for now

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.2.1-4
- Enable test again

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.2.1-3
- F-22: Rebuild for ruby 2.2
- Bootstrap, once disable test

* Sun Jan 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.2.1-2
- Enable test

* Thu Dec 18 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.2.1-1
- Initial package
