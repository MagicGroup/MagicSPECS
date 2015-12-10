%global gem_name rubypants

Name: rubygem-%{gem_name}
Version: 0.2.0
Release: 7%{?dist}
Summary: Ruby port of the smart-quotes library SmartyPants
Group: Development/Languages
License: BSD
URL: https://github.com/jmcnevin/rubypants
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Minitest 5 support
# https://github.com/jmcnevin/rubypants/pull/3
Patch0: rubygem-rubypants-0.2.0-minitest.patch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
RubyPants is a Ruby port of the smart-quotes library SmartyPants.  The
original "SmartyPants" is a free web publishing plug-in for Movable Type,
Blosxom, and BBEdit that easily translates plain ASCII punctuation characters
into "smart" typographic punctuation HTML entities.


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

# New versions of rubygems make the "author" field mandatory
sed '/s.email/ i\
  s.author = "Jeremy McNevin"' -i %{gem_name}.gemspec

# Minitest 5 support
# https://github.com/jmcnevin/rubypants/pull/3
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm -rf .%{gem_instdir}/%{gem_name}.gemspec

%install
# Note that the rubypants gem does not install the library into a "lib" folder.
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -I. test_rubypants.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README
%{gem_instdir}/rubypants.rb
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/install.rb
%exclude %{gem_instdir}/test_rubypants.rb

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.2.0-7
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.0-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.0-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 02 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.0-3
- Patch for Minitest 5 (RHBZ #1107230)
- Update upstream gem's primary author name when writing gemspec

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.0-1
- Initial package
