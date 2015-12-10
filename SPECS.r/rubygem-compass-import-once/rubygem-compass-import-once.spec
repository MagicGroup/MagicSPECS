# Generated from compass-import-once-1.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name compass-import-once

Name: rubygem-%{gem_name}
Version: 1.0.5
Release: 8%{?dist}
Summary: Speed up your Sass compilation by making @import only import each file once
Group: Development/Languages
License: MIT
URL: https://github.com/chriseppstein/compass/tree/master/import-once
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# http://github.com/compass/compass/issue/1828
# backported to compass 1.0.1
Patch0: minitest5-import-once-1.0.1.patch

BuildRequires: rubygems-devel 
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(sass)
#BuildRequires: rubygem(sass-globbing) # not yet packaged
BuildRequires: rubygem(diff-lcs)
BuildArch: noarch

%description
Changes the behavior of Sass's @import directive to only import a file once.

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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# remove uneccessary files
pushd %{buildroot}%{gem_instdir}
rm .gitignore Gemfile* *.gemspec Rakefile
popd


# Run the test suite
%check
pushd .%{gem_instdir}
sed -i '/sass-globbing/ s/^/#/' test/test_helper.rb
mv test/fixtures/with_globbing.scss{,.disable}
ruby -Ilib:test test/import_once_test.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt
%{gem_instdir}/VERSION

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/test

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.5-8
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.0.5-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.5-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Mo Morsi <mmorsi@redhat.com> - 1.0.5-4
- Remove sass-globbing dep to run tests
- Apply patch in prep section

* Wed Sep 17 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.5-3
- Run tests

* Thu Aug 28 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.5-2
- Remove uneeded Requires
- Add VERSION to main package

* Thu Aug 21 2014 Mo Morsi <mmorsi@redhat.com> - 1.0.5-1
- Initial package
