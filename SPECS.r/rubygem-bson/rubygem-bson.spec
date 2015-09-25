# Generated from bson-1.3.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bson

Summary: Ruby implementation of BSON
Name: rubygem-%{gem_name}
Version: 1.10.2
Release: 3%{?dist}
Group: Development/Languages
License: ASL 2.0 
URL: http://www.mongodb.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/mongodb/mongo-ruby-driver.git && cd mongo-ruby-driver && git checkout 1.10.2
# tar czvf bson-1.10.2-tests.tgz test/bson
Source1: %{gem_name}-%{version}-tests.tgz
# Use old test_helper.rb, which does not have unnecessary dependencies.
Source2: https://raw.github.com/mongodb/mongo-ruby-driver/ffc598c0952a37fe81e35fe52e8aa0ce695cb1dd/test/bson/test_helper.rb
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
A Ruby BSON implementation for MongoDB. For more information about Mongo, see
http://www.mongodb.org. For more information on BSON, see
http://www.bsonspec.org.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

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
# Extract tests.
tar xzf %{SOURCE1}

# Move test_helper.rb into place.
cp %{SOURCE2} test/bson

# String#to_bson_code is implemented in Mongo.
sed -i -r "s|('this.c.d < this.e')\.to_bson_code|BSON::Code.new\(\1\)|" test/bson/bson_test.rb

# StringIO is required by BSONTest#test_read_bson_document, but there is no
# point to report it upstream, since upstream switched to RSpec meanwhile.
ruby -Ilib:test/bson -e 'gem "test-unit"; Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/b2json
%{_bindir}/j2bson
%{gem_instdir}/LICENSE
%{gem_instdir}/VERSION
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/bson.gemspec


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.10.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to bson 1.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to bson 1.9.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 08 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.4-1
- Update to bson 1.6.4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.4.0-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Update to bson 1.4.0

* Wed May 25 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.1-1
- Initial package
