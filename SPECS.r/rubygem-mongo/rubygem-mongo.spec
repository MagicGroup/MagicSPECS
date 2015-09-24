%global gem_name mongo

Summary:       Ruby driver for the MongoDB
Name:          rubygem-%{gem_name}
Version:       1.10.2
Release:       3%{?dist}
License:       ASL 2.0
URL:           http://www.mongodb.org
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
# For running the tests
BuildRequires: %{_bindir}/mongod
BuildRequires: rubygem(bson)
BuildRequires: rubygem(shoulda)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(test-unit)
BuildArch:     noarch


%description
A Ruby driver for MongoDB. For more information about Mongo, see
http://www.mongodb.org.

%package doc
Summary: Documentation for %{name}
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

chmod a-x test/test_helper.rb

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* %{buildroot}%{_bindir}

%check
pushd .%{gem_instdir}

# Spawn For Ruby 1.8 should not be needed for Ruby 1.9+.
sed -i "/require 'sfl'/ d" test/tools/mongo_config.rb

# Create data directory and start testing mongo instance.
mkdir data
mongod \
  --dbpath data \
  --logpath data/log \
  --fork \
  --auth

# This should mimic the "rake test:default".
# https://github.com/mongodb/mongo-ruby-driver/blob/1.9.2/tasks/testing.rake
find test/{unit,functional,threading} -name '*_test.rb' \
  ! -wholename 'test/functional/grid_io_test.rb' \
  ! -wholename 'test/functional/grid_test.rb' \
  ! -wholename 'test/functional/ssl_test.rb' \
  | DBPATH=data JENKINS_CI=1 xargs ruby -Ilib:test

# Shutdown mongo and celanupt the data.
mongod --shutdown --dbpath data
rm -rf data
popd

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{_bindir}/mongo_console
%{gem_instdir}/bin
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/VERSION
%doc %{gem_docdir}
%{gem_instdir}/test
%{gem_instdir}/mongo.gemspec
%{gem_instdir}/Rakefile

%changelog
* Mon Jul 27 2015 Troy Dawson <tdawson@redhat.com> - 1.10.2-2
- Fix tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to mongo 1.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to mongo 1.9.2.
- Enabled test suite.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 1.6.4-4
- Fix to make it build/install on F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Troy Dawson <tdawson@redhat.com> - 1.6.4-2
- Fixed doc
- removed more BuildRequires that are not required

* Thu Aug 09 2012 Troy Dawson <tdawson@redhat.com> - 1.6.4-1
- Updated to latest version
- Removed BuildRequires that are not needed

* Thu Aug 09 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-7
- Fixed checks.  
  Only run checks that do not require a running mongodb server

* Tue Aug 07 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-6
- Changed .gemspec and Rakefile to not be doc
- Added checks

* Thu Aug 02 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-5
- Fixed rubygem(bson) requires

* Mon Jul 23 2012 Troy Dawson <tdawson@redhat.com> - 1.4.0-4
- Updated to meet new fedora rubygem guidelines

* Thu Nov 17 2011 Troy Dawson <tdawson@redhat.com> - 1.4.0-3
- Changed group to Development/Languages
- Changed the global variables
- Seperated the doc and test into the doc rpm

* Thu Nov 17 2011 Troy Dawson <tdawson@redhat.com> - 1.4.0-2
- Added %{?dist} to version

* Tue Nov 15 2011  <tdawson@redhat.com> - 1.4.0-1
- Initial package
