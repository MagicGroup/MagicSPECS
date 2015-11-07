# Generated from database_cleaner-1.4.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name database_cleaner

Name: rubygem-%{gem_name}
Version: 1.4.1
Release: 3%{?dist}
Summary: Strategies for cleaning databases
Group: Development/Languages
License: MIT
URL: http://github.com/DatabaseCleaner/database_cleaner
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: redis-test.conf
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: %{_bindir}/mongod
BuildRequires: %{_bindir}/redis-server
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(mongo)
BuildRequires: rubygem(moped)
BuildRequires: rubygem(redis)
BuildRequires: rubygem(rspec2)
BuildRequires: rubygem(sequel)
BuildRequires: rubygem(sqlite3)
BuildArch: noarch

%description
Strategies for cleaning databases. Can be used to ensure a clean state for
testing.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# https://github.com/DatabaseCleaner/database_cleaner/pull/368
chmod -x %{buildroot}%{gem_libdir}/database_cleaner/active_record/truncation.rb
chmod -x %{buildroot}%{gem_libdir}/database_cleaner/sequel/truncation.rb
chmod -x %{buildroot}%{gem_instdir}/examples/Gemfile

%check
pushd .%{gem_instdir}
# Bundler just complicates everything in our case, remove it.
sed -i '/require "bundler"/ s/^/#/' spec/spec_helper.rb
sed -i '/Bundler.setup/ s/^/#/' spec/spec_helper.rb

# Some tests fail due to changes in AR 4.0.
# https://github.com/bmabey/database_cleaner/issues/237
sed -i '/\.should_receive(:increment_open_transactions)/{s/^/#/}' spec/database_cleaner/active_record/transaction_spec.rb
sed -i '/\.should_receive(:decrement_open_transactions)/{s/^/#/}' spec/database_cleaner/active_record/transaction_spec.rb

mkdir db
cat > db/config.yml << EOF
sqlite3:
  adapter: sqlite3
  database: db/test.sqlite3
  pool: 5
  timeout: 5000
EOF

# Disable MySql and Postgres ActiveRecord adapters for now. They need more
# configuration probably.
sed -i '/active_record\/connection_adapters\/mysql/{s/^/#/}' spec/database_cleaner/active_record/truncation_spec.rb
sed -i '/active_record\/connection_adapters\/post/{s/^/#/}' spec/database_cleaner/active_record/truncation_spec.rb
sed -i 's/\[ MysqlAdapter, Mysql2Adapter, SQLite3Adapter, PostgreSQLAdapter ]/\[SQLite3Adapter\]/' \
  spec/database_cleaner/active_record/truncation_spec.rb

# Disable MySql and Postgres for Sequel.
sed -r -i '/postgres|mysql2?:\/\/\// s/^/#/' spec/database_cleaner/sequel/{deletion,truncation}_spec.rb

# Start MongoDB
mongod --dbpath=. --logpath ./mongod.log --fork

# Start a testing Redis server instance
redis-server %{SOURCE1}

rspec2 \
  spec/database_cleaner/configuration_spec.rb \
  spec/database_cleaner/active_record/*_spec.rb \
  spec/database_cleaner/active_record/truncation/sqlite3_spec.rb \
  spec/database_cleaner/generic \
  spec/database_cleaner/mongo \
  spec/database_cleaner/moped \
  spec/database_cleaner/redis \
  spec/database_cleaner/sequel \

# Quite Redis server.
kill -INT `cat db/redis.pid`

# Quit MongoDB
kill -INT `cat mongod.lock`

popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/*.yml
%{gem_instdir}/Gemfile.lock
%doc %{gem_instdir}/CONTRIBUTE.markdown
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/features
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.4.1-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.1-2
- 为 Magic 3.0 重建

* Mon Jun 22 2015 Vít Ondruch <vondruch@redhat.com> - 1.4.1-1
- Update to database_cleaner 1.4.1.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Update to database_cleaner 1.1.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.6-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 0.6.6-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Vít Ondruch <vondruch@redhat.com> - 0.6.6-2
- Fixed -doc subpackage dependency.

* Mon Mar 21 2011 Vít Ondruch <vondruch@redhat.com> - 0.6.6-1
- Updated upstream version.

* Mon Mar 21 2011 Vít Ondruch <vondruch@redhat.com> - 0.5.2-2
- Added tests.

* Wed Oct 06 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.5.2-1
- Initial package
