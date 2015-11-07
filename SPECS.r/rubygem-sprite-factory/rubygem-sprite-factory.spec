# Generated from sprite-factory-1.6.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprite-factory

Name: rubygem-%{gem_name}
Version: 1.7
Release: 3%{?dist}
Summary: Automatic CSS sprite generator
Group: Development/Languages
License: MIT
URL: https://github.com/jakesgordon/sprite-factory
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: ruby-RMagick
BuildRequires: rubygem(chunky_png)
BuildRequires: rubygem(minitest)
BuildRequires: pngcrush
BuildArch: noarch

%description
Combines individual images from a directory into a single sprite image file and creates an appropriate CSS stylesheet.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

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


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Different version of ImageMagick
# https://github.com/jakesgordon/sprite-factory/issues/37
ruby -rminitest/autorun -rrubygems -Ilib:test -e 'Dir.glob("./test/*_test.rb").sort.each { |t| require t }' | grep '11 failures, 0 errors, 0 skips'
popd

%files
%dir %{gem_instdir}
%{_bindir}/sf
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/RELEASE_NOTES.md
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/sprite_factory.gemspec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.7-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.7-2
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Josef Stribny <jstribny@redhat.com> - 1.7-1
- Update to 1.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 27 2014 Josef Stribny <jstribny@redhat.com> - 1.6.1-1
- Update to sprite-factory 1.6.1

* Fri Aug 22 2014 Josef Stribny <jstribny@redhat.com> - 1.6.0-2
- Allow 2 or 3 failures due to the unstability of the test suite

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 1.6.0-1
- Initial package
