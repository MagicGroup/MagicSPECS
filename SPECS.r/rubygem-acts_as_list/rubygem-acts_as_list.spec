# Generated from acts_as_list-0.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name acts_as_list

Name: rubygem-%{gem_name}
Version: 0.4.0
Release: 4%{?dist}
Summary: A gem allowing a active_record model to act_as_list
Group: Development/Languages
License: MIT
URL: http://github.com/swanandp/acts_as_list
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel 
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(sqlite3)
BuildArch: noarch

%description
This "acts_as" extension provides the capabilities for sorting and reordering
a number of objects in a list. The class that has this specified needs to have
a "position" column defined as an integer on the mapped database table.


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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite
%check
pushd .%{gem_instdir}
# Remove Bundler
sed -i -e '2,9d' test/helper.rb
ruby -Ilib:test -rsqlite3 test/test_list.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%license %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.md
%{gem_instdir}/test
%{gem_instdir}/init.rb
%{gem_instdir}/gemfiles
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.4.0-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.4.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.0-2
- 为 Magic 3.0 重建

* Thu Sep 18 2014 Josef Stribny <jstribny@redhat.com> - 0.4.0-1
- Initial package
