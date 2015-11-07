%global gem_name thinking-sphinx

Name: rubygem-%{gem_name}
Version: 3.1.3
Release: 4%{?dist}
Summary: A smart wrapper over Sphinx for ActiveRecord
Group: Development/Languages
License: MIT
URL: https://pat.github.io/thinking-sphinx/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: rubygem-thinking-sphinx-database.yml
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(activerecord) >= 3.1.0
Requires: rubygem(builder) >= 2.1.2
Requires: rubygem(joiner) >= 0.2.0
Requires: rubygem(middleware) >= 0.1.0
Requires: rubygem(innertube) >= 1.0.2
Requires: rubygem(riddle) >= 1.5.11
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
# %%check deps:
#BuildRequires: rubygem(rspec)
#BuildRequires: rubygem(activerecord)
#BuildRequires: mysql-server
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
An intelligent layer for ActiveRecord (via Rails and Sinatra) for the Sphinx
full-text search tool.


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

# Remove developer-only files.
for f in .gitignore .travis.yml Appraisals Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done
rm -rf gemfiles
sed -i "s|\"gemfiles/[^\"]*\",||g" %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  # The test suite requires a running mysql server (default "localhost").
  # See spec/sphinx_helper.rb and spec/fixtures/database.yml.default
  # This may not work out well within mock / koji.

  #mkdir -p /tmp/mysql/data
  #mkdir -p /tmp/mysql/log

  #mysql_install_db --ldata=/tmp/mysql/data

  #mysqld_safe \
  #--datadir=/tmp/mysql/data \
  #--pid-file=/tmp/mysql/mysql.pid \
  #--log-error=/tmp/mysql/log/mysql.log \
  #--bind-address=127.0.0.1 \
  #--socket=/tmp/mysql/mysql.sock &

  #mysqladmin \
  #--user=root \
  #--socket=/tmp/mysql/mysql.sock \
  #create thinking_sphinx

  #install -p -m 644 %%{SOURCE1} spec/fixtures/database.yml

  #rspec -Ilib spec

  #kill $(cat /tmp/mysql/mysql.pid)
popd



%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENCE
%doc %{gem_instdir}/README.textile
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/HISTORY
%exclude %{gem_instdir}/spec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.1.3-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.1.3-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.1.3-1
- Update to thinking-sphinx 3.1.3 (RHBZ #1184860)
- Use %%license macro for LICENCE file

* Wed Nov 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.1.2-1
- Update to thinking-sphinx 3.1.2 (RHBZ #1160304)

* Mon Jul 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.1.1-1
- Update to thinking-sphinx 3.1.1 (RHBZ #1090025)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 17 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.1.0-1
- Update to thinking-sphinx 3.1.0
- Remove dot-files during %%prep

* Fri Nov 08 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.6-2
- Escape macro in comments

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.6-1
- Initial package, using gem2rpm version 0.9.2
