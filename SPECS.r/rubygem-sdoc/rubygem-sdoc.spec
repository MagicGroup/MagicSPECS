# Generated from sdoc-0.3.20.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sdoc

Name: rubygem-%{gem_name}
Version: 0.4.1
Release: 5%{?dist}
Summary: RDoc generator to build searchable HTML documentation for Ruby code
Group: Development/Languages
# License needs to take RDoc and Darkfish into account apparantly
# https://github.com/voloko/sdoc/issues/27
# SDoc itself is MIT, RDoc part is (GPLv2 or Ruby) and Darkfish is BSD
License: MIT and (GPLv2 or Ruby) and BSD
URL: http://github.com/voloko/sdoc
# Let's build the gem on the latest stable release to avoid confusion
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Man pages
# https://github.com/voloko/sdoc/pull/49
Source1: sdoc.1
Source2: sdoc-merge.1
# Fix sdoc --version to return the correct version
Patch0: rubygem-sdoc-version-option-fix.patch
BuildRequires: ruby(release)
BuildRequires: rubygem(minitest)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
SDoc is simply a wrapper for the rdoc command line tool.


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

%patch0 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

# Install man pages into appropriate place.
mkdir -p %{buildroot}%{_mandir}/man1
cp %{SOURCE1} %{buildroot}%{_mandir}/man1
cp %{SOURCE2} %{buildroot}%{_mandir}/man1

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
find %{buildroot}%{gem_instdir}/lib/rdoc/generator/template -type f | xargs chmod a-x

%check
pushd .%{gem_instdir}
# Get rid of Bundler
sed -i "s/require 'bundler\/setup'//" ./spec/spec_helper.rb
# To run the tests using minitest 5
ruby -rminitest/autorun -Ilib - << \EOF
  Test = Minitest
  Dir.glob "./spec/*.rb", &method(:require)
EOF
popd

%files
%dir %{gem_instdir}
%{_bindir}/sdoc
%{_bindir}/sdoc-merge
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{_mandir}/man1/sdoc-merge.1*
%doc %{_mandir}/man1/sdoc.1*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.4.1-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.1-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 05 2015 Josef Stribny <jstribny@redhat.com> - 0.4.1-2
- Add Ruby license to licences

* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Josef Stribny <jstribny@redhat.com> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Jan 24 2014 Josef Stribny <jstribny@redhat.com> - 0.4.0-2
- Fix disttag

* Thu Jan 23 2014 Josef Stribny <jstribny@redhat.com> - 0.4.0-1
- Update to sdoc 0.4.0
- Run tests
- Fix changelog

* Mon Nov 25 2013 Josef Stribny <jstribny@redhat.com> - 0.4.0-2.rc1
- sdoc 0.4.0 git pre-release to support RDoc 4.0

* Wed Nov 06 2013 Josef Stribny <jstribny@redhat.com> - 0.4.0-1.rc1
- sdoc 0.4.0 git pre-release to support RDoc 4.0

* Tue Aug 06 2013 Josef Stribny <jstribny@redhat.com> - 0.3.20-2
- Add man pages

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 0.3.20-1
- Initial package
