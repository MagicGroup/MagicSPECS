# Generated from pg-0.11.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name pg

Summary: A Ruby interface to the PostgreSQL RDBMS
Name: rubygem-%{gem_name}
Version: 0.18.2
Release: 4%{?dist}
Group: Development/Languages
# Upstream license clarification (https://bitbucket.org/ged/ruby-pg/issue/72/)
#
# The portions of the code that are BSD-licensed are licensed under
# the BSD 3-Clause license; the contents of the BSD file are incorrect.
#
License: (BSD or Ruby) and PostgreSQL
URL: http://bitbucket.org/ged/ruby-pg/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Disable RPATH.
# https://bitbucket.org/ged/ruby-pg/issue/183
Patch0: rubygem-pg-0.17.1-remove-rpath.patch
BuildRequires: ruby(release)
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: postgresql-server postgresql-devel
BuildRequires: rubygem(rspec)
# Introduced in F17.
Obsoletes: ruby(postgres) <= 0.7.9-2010.01.28.2

%description
This is the extension library to access a PostgreSQL database from Ruby.
This library works with PostgreSQL 7.4 and later.


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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext

# Remove useless shebangs.
sed -i -e '/^#!\/usr\/bin\/env/d' %{buildroot}%{gem_instdir}/Rakefile
sed -i -e '/^#!\/usr\/bin\/env/d' %{buildroot}%{gem_instdir}/Rakefile.cross

# Files under %%{gem_libdir} are not executable.
for file in `find %{buildroot}%{gem_libdir} -type f -name "*.rb"`; do
    sed -i '/^#!\/usr\/bin\/env/ d' $file \
    && chmod -v 644 $file
done

# Fix shebangs and executable bits of samples.
for file in `find %{buildroot}%{gem_instdir}/sample -type f -name "*.rb"`; do
    sed -i -e '/^#!\/usr\/bin\/env/ s/.*/#!\/usr\/bin\/ruby/' $file \
    && chmod -v 755 $file
done

# Fix spec shebangs.
# https://bitbucket.org/ged/ruby-pg/issue/74/
for file in `find %{buildroot}%{gem_instdir}/spec -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] \
        && sed -i -e 's/^#!\/usr\/bin\/env spec/#!\/usr\/bin\/env rspec/' $file \
        && chmod -v 755 $file
done

%check
pushd .%{gem_instdir}
rspec -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%exclude %{gem_instdir}/.gemtest
%{gem_extdir_mri}
%dir %{gem_instdir}
%doc %{gem_instdir}/BSDL
%doc %{gem_instdir}/POSTGRES
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/Contributors.rdoc
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/Rakefile
%{gem_instdir}/Rakefile.cross
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/README.ja.rdoc
%doc %{gem_instdir}/README-OS_X.rdoc
%doc %{gem_instdir}/README-Windows.rdoc
%{gem_instdir}/sample
%{gem_instdir}/spec


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.18.2-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.18.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.18.2-2
- 为 Magic 3.0 重建

* Wed Aug 26 2015 Vít Ondruch <vondruch@redhat.com> - 0.18.2-1
- Update to pg 1.18.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.18.1-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Update to pg 0.18.1.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.17.1-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Update to pg 0.17.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 0.14.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to pg 0.14.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 0.12.2-2
- Obsolete ruby-postgress, which was retired.

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 0.12.2-1
- Rebuilt for Ruby 1.9.3.
- Upgrade to pg 0.12.2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-5
- Pass CFLAGS to extconf.rb.

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-4
- Binary extension moved into ruby_sitearch dir.
- -doc subpackage made architecture independent.

* Wed Jun 01 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-3
- Quoted upstream license clarification.

* Mon May 30 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-2
- Removed/fixed shebang in non-executables.
- Removed sources.

* Thu May 26 2011 Vít Ondruch <vondruch@redhat.com> - 0.11.0-1
- Initial package
