%global gem_name riddle

Name: rubygem-%{gem_name}
Version: 1.5.11
Release: 4%{?dist}
Summary: An API for Sphinx, written in and for Ruby
Group: Development/Languages
License: MIT
URL: http://pat.github.io/riddle/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(mysql2)
BuildRequires: rubygem(yard)
# %%check deps:
#BuildRequires: rubygem(rspec)
#BuildRequires: mysql-server
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
A Ruby API and configuration helper for the Sphinx search service.


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
for f in .gitignore .travis.yml Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  # The test suite requires a running mysql server (default "localhost")
  # with a user (default "anonymous") who has privs to create databases.
  # See spec/support/sphinx.rb and spec/fixtures/sql/conf.example.yml
  # This may not work out well within mock / koji.
  #rspec -Ilib spec
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENCE
%doc %{gem_instdir}/README.textile
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/HISTORY
%exclude %{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.5.11-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.11-1
- Update to riddle 1.5.11 (RHBZ #1090027)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sat Jan 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.10-1
- Update to riddle 1.5.10
- Remove dot-files during %%prep

* Wed Oct 30 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.9-1
- Update to riddle 1.5.9
- Remove Gemfile and Rakefile
- Exclude tests from binary pkgs
