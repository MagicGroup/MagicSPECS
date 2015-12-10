%global gem_name fast_xs

Name: rubygem-%{gem_name}
Version: 0.8.0
Release: 11%{?dist}
Summary: Provides C extensions for escaping text
Group: Development/Languages
License: MIT 
URL: http://fast-xs.rubyforge.org/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby-devel 

%description
fast_xs provides C extensions for escaping text.
The original String#fast_xs method is based on the xchar code by Sam Ruby:
* http://intertwingly.net/stories/2005/09/28/xchar.rb
* http://intertwingly.net/blog/2005/09/28/XML-Cleansing
_why also packages an older version with Hpricot (patches submitted).
The version here should be compatible with the latest version of Hpricot
code.
Ruby on Rails will automatically use String#fast_xs from either Hpricot
or this gem version with the bundled Builder package.
String#fast_xs is an almost exact translation of Sam Ruby's original
implementation (String#to_xs), but it does escape "&quot;" (which is an
optional, but all parsers are able ot handle it.  XML::Builder as
packaged in Rails 2.0 will be automatically use String#fast_xs instead
of String#to_xs available.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%rubygems_default_filter
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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

rm %{buildroot}%{gem_instdir}/.gitignore

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.rdoc
 
%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/History.rdoc
%{gem_instdir}/GNUmakefile
%{gem_instdir}/Rakefile
%{gem_instdir}/setup.rb
%{gem_instdir}/test

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.8.0-11
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.0-10
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.0-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Vít Ondruch <vondruch@redhat.com> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Aug 07 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.0-3
- 987457 - better formating of description
- 987457 - escape macro in comment

* Tue Jul 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.0-2
- move rubygem-filter macro after description (msuchy@redhat.com)
- polish spec before review (msuchy@redhat.com)
- filter so files from provides (msuchy@redhat.com)

* Mon Jul 22 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.0-1
- initial package (created by gem2rpm)

