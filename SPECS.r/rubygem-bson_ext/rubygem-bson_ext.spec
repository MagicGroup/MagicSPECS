# Generated from bson_ext-1.3.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bson_ext


Summary: C extensions for Ruby BSON
Name: rubygem-%{gem_name}
Version: 1.10.2
Release: 6%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://www.mongodb.org/display/DOCS/BSON

Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/mongodb/mongo-ruby-driver.git && cd mongo-ruby-driver && git checkout 1.10.2
# tar czvf bson_ext-1.10.2-tests.tgz test/bson
Source1: %{gem_name}-%{version}-tests.tgz
# Use old test_helper.rb, which does not have unnecessary dependencies.
Source2: https://raw.github.com/mongodb/mongo-ruby-driver/ffc598c0952a37fe81e35fe52e8aa0ce695cb1dd/test/bson/test_helper.rb

BuildRequires: ruby-devel
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# for tests:
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(bson) >= 1.9.0
BuildRequires: rubygem(json)
BuildRequires: rubygem(test-unit)


%description
C extensions to accelerate the Ruby BSON serialization. For more information
about BSON, see http://bsonspec.org.  For information about MongoDB, see
http://www.mongodb.org.


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

%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/bson_ext
cp -a {.%{gem_extdir_mri},%{buildroot}%{gem_extdir_mri}}/bson_ext/*.so
cp -a {.%{gem_extdir_mri},%{buildroot}%{gem_extdir_mri}}/gem.build_complete

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext


%check
pushd .%{gem_instdir}
# Extract tests.
tar xzvf %{SOURCE1}

# Move test_helper.rb into place.
cp %{SOURCE2} test/bson

# Remove the inclusion of bson (absolute path that doesn't exist) and rather require it while running ruby
sed -i "/require File.join(File.dirname(__FILE__), '..', '..', 'lib', 'bson')/d" test/bson/test_helper.rb

# String#to_bson_code is implemented in Mongo.
sed -i -r "s|('this.c.d < this.e')\.to_bson_code|BSON::Code.new\(\1\)|" test/bson/bson_test.rb

# https://jira.mongodb.org/browse/RUBY-466
%ifarch i686 %{arm}
sed -i "/^  def test_date_before_epoch$/,/^  end$/ s/^/#/" test/bson/bson_test.rb
%endif

# StringIO is required by BSONTest#test_read_bson_document, but there is no
# point to report it upstream, since upstream switched to RSpec meanwhile.
ruby -I$(dirs +1)%{gem_extdir_mri}:test/bson -rbson -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd


%files
%dir %{gem_instdir}
%{gem_instdir}/LICENSE
%exclude %{gem_cache}
%{gem_spec}
%{gem_extdir_mri}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/VERSION
%{gem_instdir}/bson_ext.gemspec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.10.2-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.10.2-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to bson_ext 1.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Vít Ondruch <vondruch@redhat.com> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Nov 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-2
- Properly fix ARM build.

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to bson_ext 1.9.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 08 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.4-1
- Update to bson_ext 1.6.4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.4.0-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 bkabrda <bkabrda@redhat.com> - 1.4.0-2
- Moved test cleanup to check section.

* Thu Sep 22 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-1
- Version 1.4.0 (removed the fix for failing tests, as it is now in upstream).

* Tue Sep 20 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.1-2
- Added the fix for failing tests on i386 (should be fixed in 1.4.0, so it can be removed then) -
  see https://github.com/mongodb/mongo-ruby-driver/commit/e613880922beaf1e80274aa183aa5ac0a9d09ac4

* Thu Sep 08 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.1-1
- Initial package
