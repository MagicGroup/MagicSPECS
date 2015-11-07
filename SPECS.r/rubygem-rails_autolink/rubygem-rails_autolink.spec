%global gem_name rails_autolink

Name: rubygem-%{gem_name}
Version: 1.1.6
Release: 3%{?dist}
Summary: Automatic generation of HTML links in texts
Group: Development/Languages
License: MIT
URL: https://github.com/tenderlove/rails_autolink
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(rails) > 3.1
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rails) > 3.1
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
This is an extraction of the `auto_link` method from rails. The `auto_link`
method was removed from Rails in version Rails 3.1. This gem is meant to
bridge the gap for people migrating.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Remove developer-only files.
for f in Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove extra gemspec file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.rdoc
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%exclude %{gem_instdir}/test


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.6-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.6-2
- 为 Magic 3.0 重建

* Wed Jun 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.6-1
- Drop upstreamed timeout patch
- Update to 1.1.6 (RHBZ #1106463)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Adjustments for Minitest 5 (RHBZ #1107206)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 07 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.5-1
- Update to 1.1.5
- Remove Gemfile and Rakefile in %%prep
- Patch to add "require timeout" in tests

* Tue Nov 05 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.4-2
- Exclude Gemfile, Gemfile.lock, Rakefile, and test suite from the binary
  packages

* Tue Oct 08 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.4-1
- Initial package
